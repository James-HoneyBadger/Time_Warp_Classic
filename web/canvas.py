"""Server-side raster canvas for the web IDE.

The turtle code draws through a small Tk-like API.  :class:`RasterCanvas`
accepts those calls and turns them into something a browser can display
cheaply:

* straight, filled shapes are *rasterised* into a palette-indexed pixel buffer;
* the frames sent to the browser are **run-length encoded** (a run is a 16-bit
  count plus an 8-bit palette index), and only the rectangle that changed since
  the previous frame is included;
* shapes that must stay crisp - the turtle marker, tagged game objects and
  text - travel in a small vector ``overlay`` instead of being rasterised.

The result is a compact, streamable snapshot: a 600x400 canvas costs a few
hundred bytes per update instead of 240 000 pixels.
"""

from __future__ import annotations

import base64
import math
import time
from dataclasses import dataclass, field

DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 400
# White "paper": the default pen colour is black, exactly as on a classic
# turtle screen, so a dark background would hide the drawing.
DEFAULT_BACKGROUND = "#ffffff"

# At most this many overlay shapes are kept; older ones are dropped so a long
# game loop cannot grow the frame without bound.
MAX_OVERLAY_ITEMS = 200

# Seconds between streamed frames while a program is drawing.
DEFAULT_INTERVAL = 0.04


@dataclass
class _Op:
    """One canvas item."""

    kind: str
    coords: tuple = ()
    fill: str | None = None
    outline: str | None = None
    width: int = 1
    tags: tuple = field(default_factory=tuple)
    text: str = ""
    size: int = 12
    ident: int = 0


def _colour(value):
    """Normalise a Tk colour argument; ``""`` and None mean "no colour"."""
    if not value:
        return None
    if isinstance(value, (tuple, list)):
        return None
    text = str(value).strip()
    return text or None


def _number(value):
    """Coerce canvas coordinates to rounded integers."""
    return int(round(float(value)))


class RasterCanvas:
    """A tiny stand-in for a Tk canvas that draws into a pixel buffer."""

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                 background=DEFAULT_BACKGROUND, on_change=None,
                 min_interval=DEFAULT_INTERVAL):
        self.width = int(width)
        self.height = int(height)
        self._background = _colour(background) or DEFAULT_BACKGROUND
        self._on_change = on_change
        self._min_interval = min_interval
        self._last_emit = 0.0

        self._palette = [self._background]
        self._palette_index = {self._background: 0}
        self._pixels = bytearray(self.width * self.height)

        self._ops = []            # rasterised shapes, in draw order
        self._overlay = {}        # ident -> _Op drawn by the browser
        self._next_ident = 0

        self._dirty = None        # (x0, y0, x1, y1) inclusive
        self._full_dirty = False
        self._needs_redraw = False
        self._overlay_changed = False

    # ------------------------------------------------------------------
    # Tk-compatible surface used by the interpreter
    # ------------------------------------------------------------------

    def winfo_width(self):
        return self.width

    def winfo_height(self):
        return self.height

    def update_idletasks(self):
        """Tk flushes pending redraws here; there is nothing to flush."""

    def bind(self, _sequence, _callback=None):
        """Tk resize hook; the raster size is fixed, so this is a no-op."""

    def create_line(self, *coords, **kwargs):
        return self._create("line", coords, kwargs)

    def create_polygon(self, *coords, **kwargs):
        return self._create("polygon", coords, kwargs)

    def create_oval(self, *coords, **kwargs):
        return self._create("oval", coords, kwargs)

    def create_rectangle(self, *coords, **kwargs):
        return self._create("rectangle", coords, kwargs)

    def create_text(self, *coords, **kwargs):
        return self._create("text", coords, kwargs)

    def create_image(self, *coords, **kwargs):
        """Image items are not rasterised; keep the id so deletes still work."""
        return self._create("image", coords, kwargs)

    def delete(self, target):
        """Delete by id, by tag, or everything (``"all"``)."""
        if target == "all":
            self.clear()
            return

        if isinstance(target, str):
            dropped = [op for op in self._overlay.values() if target in op.tags]
            for op in dropped:
                self._overlay.pop(op.ident, None)
            painted = [op for op in self._ops if target in op.tags]
            if painted:
                self._ops = [op for op in self._ops if target not in op.tags]
                self._needs_redraw = True
            if dropped or painted:
                self._overlay_changed = True
                self._changed()
            return

        if self._overlay.pop(target, None) is not None:
            self._overlay_changed = True
            self._changed()
            return

        for index, op in enumerate(self._ops):
            if op.ident == target:
                del self._ops[index]
                self._needs_redraw = True
                self._changed()
                return

    def clear(self):
        """Wipe the canvas back to its background."""
        self._pixels = bytearray(self.width * self.height)
        self._ops = []
        self._overlay = {}
        self._dirty = None
        self._full_dirty = True
        self._needs_redraw = False
        self._overlay_changed = True
        self._changed()

    # ------------------------------------------------------------------
    # Frames
    # ------------------------------------------------------------------

    @property
    def has_drawing(self):
        """True once anything has been drawn (pixels or overlay)."""
        return bool(self._ops or self._overlay)

    def frame(self, force=False):
        """Return the next frame, or None when nothing changed.

        ``force`` always returns a full-canvas frame, which is what the final
        frame of a run uses so the browser can resynchronise.
        """
        if self._needs_redraw:
            self._render_all()

        if force or self._full_dirty:
            rect = (0, 0, self.width - 1, self.height - 1)
            self._dirty = None
            self._full_dirty = False
        elif self._dirty is not None:
            rect = self._clamp(self._dirty)
            self._dirty = None
        elif self._overlay_changed:
            rect = None
        else:
            return None

        self._overlay_changed = False
        frame = self._base_frame(rect)
        self._last_emit = time.monotonic()
        return frame

    def _base_frame(self, rect):
        if rect is None:
            x = y = w = h = 0
            payload = ""
        else:
            x0, y0, x1, y1 = rect
            x, y = x0, y0
            w = max(0, x1 - x0 + 1)
            h = max(0, y1 - y0 + 1)
            payload = _encode_region(self._pixels, self.width, x, y, w, h)

        return {
            "type": "canvas",
            "width": self.width,
            "height": self.height,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "palette": list(self._palette),
            "rle": payload,
            "overlay": [self._overlay_json(op) for op in self._overlay.values()],
        }

    def _overlay_json(self, op):
        data = {"kind": op.kind}
        if op.kind == "text":
            data["x"] = _number(op.coords[0])
            data["y"] = _number(op.coords[1])
            data["text"] = op.text
            data["size"] = op.size
        else:
            data["points"] = [[_number(op.coords[i]), _number(op.coords[i + 1])]
                              for i in range(0, len(op.coords) - 1, 2)]
        data["fill"] = op.fill
        data["outline"] = op.outline or op.fill
        data["width"] = op.width
        return data

    # ------------------------------------------------------------------
    # Item creation and rasterising
    # ------------------------------------------------------------------

    def _create(self, kind, coords, kwargs):
        self._next_ident += 1
        tags = kwargs.get("tags") or ()
        if isinstance(tags, str):
            tags = (tags,)
        op = _Op(
            kind=kind,
            coords=tuple(coords),
            fill=_colour(kwargs.get("fill")),
            outline=_colour(kwargs.get("outline")),
            width=max(1, _number(kwargs.get("width") or 1)),
            tags=tuple(tags),
            text=str(kwargs.get("text") or ""),
            size=_text_size(kwargs.get("font")),
            ident=self._next_ident,
        )

        # Tagged shapes and text are drawn by the browser so they stay crisp
        # (and so moving them does not force a full repaint).
        if op.tags or kind in ("text", "image"):
            self._overlay[op.ident] = op
            self._overlay_changed = True
            self._trim_overlay()
            self._changed()
            return op.ident

        self._ops.append(op)
        if not self._needs_redraw:
            self._paint(op)
        self._changed()
        return op.ident

    def _trim_overlay(self):
        while len(self._overlay) > MAX_OVERLAY_ITEMS:
            self._overlay.pop(next(iter(self._overlay)))

    def _render_all(self):
        self._pixels = bytearray(self.width * self.height)
        for op in self._ops:
            self._paint(op)
        self._needs_redraw = False
        self._full_dirty = True

    def _paint(self, op):
        """Draw one shape into the pixel buffer and grow the dirty rect."""
        if op.kind == "line":
            if len(op.coords) < 4:
                return
            index = self._index(op.fill)
            x0, y0, x1, y1 = (_number(value) for value in op.coords[:4])
            self._line(x0, y0, x1, y1, index, op.width)
            self._touch(x0, y0, x1, y1, op.width)
        elif op.kind == "rectangle":
            if len(op.coords) < 4:
                return
            x0, y0, x1, y1 = (_number(value) for value in op.coords[:4])
            self._rectangle(x0, y0, x1, y1, op.fill, op.outline, op.width)
            self._touch(x0, y0, x1, y1, op.width)
        elif op.kind == "oval":
            if len(op.coords) < 4:
                return
            x0, y0, x1, y1 = (_number(value) for value in op.coords[:4])
            self._oval(x0, y0, x1, y1, op.fill, op.outline, op.width)
            self._touch(x0, y0, x1, y1, op.width)
        elif op.kind == "polygon":
            points = [_number(value) for value in op.coords]
            if len(points) < 6:
                return
            self._polygon(points, op.fill, op.outline, op.width)
            xs = points[0::2]
            ys = points[1::2]
            self._touch(min(xs), min(ys), max(xs), max(ys), op.width)

    # ---- pixel helpers ------------------------------------------------

    def _index(self, colour):
        if colour is None:
            return 0
        if colour in self._palette_index:
            return self._palette_index[colour]
        if len(self._palette) >= 255:
            return self._palette_index.get(colour, 0)
        self._palette.append(colour)
        index = len(self._palette) - 1
        self._palette_index[colour] = index
        return index

    def _put(self, x, y, index):
        if 0 <= x < self.width and 0 <= y < self.height:
            self._pixels[y * self.width + x] = index

    def _stamp(self, x, y, index, width):
        """Plot a dot of *width* pixels centred on (x, y)."""
        if width <= 1:
            self._put(x, y, index)
            return
        half = width // 2
        for dy in range(-half, width - half):
            for dx in range(-half, width - half):
                self._put(x + dx, y + dy, index)

    def _line(self, x0, y0, x1, y1, index, width=1):
        """Bresenham line, stamped with the pen width."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        error = dx + dy
        while True:
            self._stamp(x0, y0, index, width)
            if x0 == x1 and y0 == y1:
                break
            doubled = 2 * error
            if doubled >= dy:
                error += dy
                x0 += sx
            if doubled <= dx:
                error += dx
                y0 += sy

    def _hline(self, x0, x1, y, index):
        if y < 0 or y >= self.height:
            return
        start = max(0, min(x0, x1))
        end = min(self.width - 1, max(x0, x1))
        if start > end:
            return
        base = y * self.width
        self._pixels[base + start:base + end + 1] = bytes([index]) * (end - start + 1)

    def _rectangle(self, x0, y0, x1, y1, fill, outline, width):
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        if fill is not None:
            index = self._index(fill)
            for y in range(y0, y1 + 1):
                self._hline(x0, x1, y, index)
        if outline is not None:
            index = self._index(outline)
            for offset in range(width):
                self._line(x0 + offset, y0 + offset, x1 - offset, y0 + offset, index)
                self._line(x0 + offset, y1 - offset, x1 - offset, y1 - offset, index)
                self._line(x0 + offset, y0 + offset, x0 + offset, y1 - offset, index)
                self._line(x1 - offset, y0 + offset, x1 - offset, y1 - offset, index)

    def _oval(self, x0, y0, x1, y1, fill, outline, width):
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        radius_x = (x1 - x0) / 2
        radius_y = (y1 - y0) / 2
        if radius_x <= 0 or radius_y <= 0:
            return
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        if fill is not None:
            index = self._index(fill)
            for y in range(y0, y1 + 1):
                offset = (y - center_y) / radius_y
                inside = 1 - offset * offset
                if inside < 0:
                    continue
                half = radius_x * math.sqrt(inside)
                self._hline(int(round(center_x - half)), int(round(center_x + half)), y, index)

        if outline is not None:
            index = self._index(outline)
            steps = max(24, int(2 * math.pi * max(radius_x, radius_y)))
            for step in range(steps):
                angle = 2 * math.pi * step / steps
                x = center_x + radius_x * math.cos(angle)
                y = center_y + radius_y * math.sin(angle)
                self._stamp(int(round(x)), int(round(y)), index, width)

    def _polygon(self, points, fill, outline, width):
        xs = points[0::2]
        ys = points[1::2]
        if fill is not None:
            index = self._index(fill)
            top, bottom = min(ys), max(ys)
            for y in range(top, bottom + 1):
                crossings = []
                for i in range(len(xs)):
                    x_a, y_a = xs[i], ys[i]
                    x_b, y_b = xs[(i + 1) % len(xs)], ys[(i + 1) % len(xs)]
                    if (y_a <= y < y_b) or (y_b <= y < y_a):
                        ratio = (y - y_a) / (y_b - y_a)
                        crossings.append(x_a + ratio * (x_b - x_a))
                crossings.sort()
                for start, end in zip(crossings[0::2], crossings[1::2]):
                    self._hline(int(round(start)), int(round(end)), y, index)

        if outline is not None:
            index = self._index(outline)
            for i in range(len(xs)):
                x_a, y_a = xs[i], ys[i]
                x_b, y_b = xs[(i + 1) % len(xs)], ys[(i + 1) % len(xs)]
                self._line(x_a, y_a, x_b, y_b, index, width)

    # ---- dirty tracking ----------------------------------------------

    def _touch(self, x0, y0, x1, y1, width=1):
        pad = max(0, width)
        self._touch_raw(x0 - pad, y0 - pad, x1 + pad, y1 + pad)

    def _touch_raw(self, x0, y0, x1, y1):
        x0, x1 = sorted((int(x0), int(x1)))
        y0, y1 = sorted((int(y0), int(y1)))
        if self._dirty is None:
            self._dirty = (x0, y0, x1, y1)
        else:
            dx0, dy0, dx1, dy1 = self._dirty
            self._dirty = (min(dx0, x0), min(dy0, y0), max(dx1, x1), max(dy1, y1))

    def _clamp(self, rect):
        x0, y0, x1, y1 = rect
        return (
            max(0, x0), max(0, y0),
            min(self.width - 1, x1), min(self.height - 1, y1),
        )

    def _changed(self):
        """Notify the host, at most every ``min_interval`` seconds."""
        if self._on_change is None:
            return
        if time.monotonic() - self._last_emit < self._min_interval:
            return
        frame = self.frame()
        if frame is not None:
            self._on_change(frame)


def _text_size(font):
    """Pull the point size out of a Tk font spec ("Arial 14" or ("Arial", 14))."""
    if isinstance(font, (tuple, list)) and len(font) >= 2:
        try:
            return int(font[1])
        except (TypeError, ValueError):
            return 12
    if isinstance(font, str):
        parts = font.replace("-", " ").split()
        for part in reversed(parts):
            if part.isdigit():
                return int(part)
    return 12


def _encode_region(pixels, stride, x, y, width, height):
    """Run-length encode a rectangle of palette indices.

    Each run is a little-endian 16-bit count followed by the 8-bit index,
    base64-encoded for transport inside a JSON event.
    """
    if width <= 0 or height <= 0:
        return ""
    data = bytearray()
    for row in range(y, y + height):
        base = row * stride
        cursor = x
        end = x + width
        while cursor < end:
            index = pixels[base + cursor]
            run = 1
            limit = min(65535, end - cursor)
            while run < limit and pixels[base + cursor + run] == index:
                run += 1
            data += run.to_bytes(2, "little")
            data.append(index)
            cursor += run
    return base64.b64encode(bytes(data)).decode("ascii")


def decode_rle(payload, width, height):
    """Decode a frame payload into a ``width`` x ``height`` index grid."""
    pixels = bytearray(width * height)
    raw = base64.b64decode(payload) if payload else b""
    cursor = 0
    column = 0
    row = 0
    while cursor + 2 < len(raw):
        run = int.from_bytes(raw[cursor:cursor + 2], "little")
        index = raw[cursor + 2]
        cursor += 3
        for _ in range(run):
            if row < height and column < width:
                pixels[row * width + column] = index
            column += 1
            if column >= width:
                column = 0
                row += 1
    return pixels
