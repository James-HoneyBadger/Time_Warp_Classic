"""Tests for the web canvas: rasterising, dirty rectangles and RLE frames."""

import base64

from web.canvas import RasterCanvas, decode_rle


def _pixels(frame):
    """Decode a frame's RLE payload into a flat index grid."""
    return decode_rle(frame["rle"], frame["w"], frame["h"])


def _index_of(frame, colour):
    return frame["palette"].index(colour)


# ------------------------------------------------------------------ frames

def test_empty_canvas_has_no_frame_until_forced():
    canvas = RasterCanvas(40, 30)

    assert canvas.has_drawing is False
    assert canvas.frame() is None

    frame = canvas.frame(force=True)
    assert frame["width"] == 40 and frame["height"] == 30
    assert frame["palette"][0] == "#ffffff"
    assert set(_pixels(frame)) == {0}  # all background


def test_line_is_rasterised_into_the_dirty_rectangle():
    canvas = RasterCanvas(40, 30)
    canvas.create_line(5, 10, 20, 10, fill="#ff0000", width=1)

    frame = canvas.frame()

    assert frame is not None
    assert (frame["x"], frame["y"], frame["w"], frame["h"]) == (4, 9, 18, 3)
    assert frame["palette"] == ["#ffffff", "#ff0000"]

    grid = _pixels(frame)
    red = _index_of(frame, "#ff0000")
    # Local coordinates inside the sent rectangle (origin 4,9).
    assert grid[1 * frame["w"] + 1] == red      # (5,10)
    assert grid[1 * frame["w"] + 16] == red     # (20,10)


def test_frame_is_delta_after_the_first_one():
    canvas = RasterCanvas(40, 30)
    canvas.create_line(0, 0, 5, 0, fill="#000000")
    canvas.frame()

    canvas.create_line(20, 20, 25, 20, fill="#000000")
    second = canvas.frame()

    assert (second["x"], second["y"], second["w"], second["h"]) == (19, 19, 8, 3)

    full = canvas.frame(force=True)
    assert full["w"] == canvas.width and full["h"] == canvas.height
    assert second["w"] < full["w"]  # a delta, not the whole canvas


def test_no_change_returns_no_frame():
    canvas = RasterCanvas(20, 20)
    canvas.create_line(1, 1, 5, 1, fill="#000000")
    canvas.frame()

    assert canvas.frame() is None


def test_filled_rectangle_and_oval_paint_interiors():
    canvas = RasterCanvas(40, 40)
    canvas.create_rectangle(2, 2, 12, 12, fill="#00ff00")
    canvas.create_oval(20, 20, 38, 38, fill="#0000ff")

    frame = canvas.frame(force=True)
    grid = _pixels(frame)
    green = _index_of(frame, "#00ff00")
    blue = _index_of(frame, "#0000ff")
    width = frame["w"]

    assert grid[7 * width + 7] == green    # inside the rectangle
    assert grid[29 * width + 29] == blue   # centre of the oval
    assert grid[0] == 0                    # untouched corner stays background


def test_palette_reuses_a_colour():
    canvas = RasterCanvas(20, 20)
    canvas.create_line(1, 1, 5, 1, fill="#123456")
    canvas.create_line(1, 5, 5, 5, fill="#123456")

    frame = canvas.frame(force=True)

    assert frame["palette"].count("#123456") == 1


def test_overlay_holds_tagged_shapes_and_text():
    canvas = RasterCanvas(40, 30)
    canvas.create_polygon(5, 5, 10, 5, 7, 10, fill="green", outline="darkgreen",
                          width=2, tags="turtle")
    canvas.create_text(4, 6, text="hi", font=("Arial", 14), fill="#111111")

    frame = canvas.frame()

    assert len(frame["overlay"]) == 2
    kinds = {item["kind"] for item in frame["overlay"]}
    assert kinds == {"polygon", "text"}
    text = next(item for item in frame["overlay"] if item["kind"] == "text")
    assert text["text"] == "hi" and text["size"] == 14

    # The turtle is not baked into the pixels, so moving it never repaints.
    canvas.create_line(1, 1, 3, 1, fill="#000000")
    frame = canvas.frame()
    assert frame["w"] < 40  # only the line was re-sent


def test_deleting_the_turtle_removes_only_the_overlay():
    canvas = RasterCanvas(40, 30)
    canvas.create_line(0, 10, 39, 10, fill="#000000")
    canvas.create_polygon(1, 1, 4, 1, 2, 4, tags="turtle")
    canvas.frame()

    canvas.delete("turtle")
    frame = canvas.frame()

    assert frame["overlay"] == []
    assert frame["w"] == 0 and frame["h"] == 0  # nothing to repaint


def test_delete_all_clears_the_canvas():
    canvas = RasterCanvas(30, 20)
    canvas.create_rectangle(0, 0, 29, 19, fill="#ff00ff")
    canvas.frame()

    canvas.delete("all")
    frame = canvas.frame()

    assert frame is not None
    assert frame["overlay"] == []
    assert set(_pixels(frame)) == {0}
    assert canvas.has_drawing is False


def test_deleting_an_item_repaints_the_rest():
    canvas = RasterCanvas(30, 20)
    first = canvas.create_line(2, 2, 10, 2, fill="#000000")
    canvas.create_line(2, 6, 10, 6, fill="#ff0000")
    canvas.frame()

    canvas.delete(first)
    frame = canvas.frame(force=True)
    grid = _pixels(frame)
    black = _index_of(frame, "#000000") if "#000000" in frame["palette"] else None

    # The black line is gone; the red one survives.
    assert black is None or black not in grid
    assert _index_of(frame, "#ff0000") in grid


def test_frame_payload_is_base64_rle():
    canvas = RasterCanvas(10, 5)
    canvas.create_line(0, 0, 9, 0, fill="#000000")

    frame = canvas.frame()
    raw = base64.b64decode(frame["rle"])

    assert len(raw) % 3 == 0
    run = int.from_bytes(raw[0:2], "little")
    assert run >= 1


# ------------------------------------------------------------- integration

def test_logo_program_draws_on_the_canvas():
    from web.server import RunnerService

    result = RunnerService().run("logo", "FD 100\nRIGHT 90\nFD 50")

    canvas = result["canvas"]
    assert canvas is not None
    assert canvas["w"] > 0 and canvas["h"] > 0
    assert any(item["kind"] == "polygon" for item in canvas["overlay"])


def test_program_without_graphics_has_no_canvas():
    from web.server import RunnerService

    assert RunnerService().run("basic", '10 PRINT "hi"')["canvas"] is None
