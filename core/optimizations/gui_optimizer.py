#!/usr/bin/env python3
"""
GUI optimization for Time_Warp_Classic.

This module provides GUI performance enhancements including:
- Asynchronous UI updates
- UI thread management
- Rendering optimizations
- Event handling improvements
"""

import threading
import queue
import time
from typing import Callable, Any, Optional, Dict, List
from functools import partial
import tkinter as tk


class UIThreadManager:
    """Manages UI operations to prevent blocking the main thread."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.task_queue: queue.Queue[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = queue.Queue()
        self.worker_thread: Optional[threading.Thread] = None
        self.running = False
        self._lock = threading.RLock()

    def start(self) -> None:
        """Start the UI thread manager."""
        with self._lock:
            if not self.running:
                self.running = True
                self.worker_thread = threading.Thread(target=self._process_tasks, daemon=True)
                self.worker_thread.start()

    def stop(self) -> None:
        """Stop the UI thread manager."""
        with self._lock:
            self.running = False
            if self.worker_thread:
                self.worker_thread.join(timeout=1.0)

    def schedule_task(self, task: Callable, *args, **kwargs) -> None:
        """Schedule a task to run asynchronously."""
        if self.running:
            self.task_queue.put((task, args, kwargs))

    def _process_tasks(self) -> None:
        """Process tasks in the worker thread."""
        while self.running:
            try:
                task, args, kwargs = self.task_queue.get(timeout=0.1)
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    print(f"UI task error: {e}")
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def call_soon(self, callback: Callable, *args) -> None:
        """Schedule a callback to run in the main thread."""
        self.root.after(0, callback, *args)


class AsyncTextUpdate:
    """Asynchronous text widget updates to prevent UI freezing."""

    def __init__(self, text_widget: tk.Text, max_buffer_size: int = 1000):
        self.text_widget = text_widget
        self.update_queue: queue.Queue[tuple[str, tuple[Any, ...], dict[str, Any]]] = queue.Queue()
        self.max_buffer_size = max_buffer_size
        self.updating = False
        self._lock = threading.RLock()

    def queue_update(self, operation: str, *args, **kwargs) -> None:
        """Queue a text update operation."""
        with self._lock:
            if self.update_queue.qsize() < self.max_buffer_size:
                self.update_queue.put((operation, args, kwargs))
                if not self.updating:
                    self._schedule_next_update()

    def _schedule_next_update(self) -> None:
        """Schedule the next update in the main thread."""
        if not self.updating and not self.update_queue.empty():
            self.updating = True
            self.text_widget.after(1, self._process_update)

    def _process_update(self) -> None:
        """Process the next update."""
        try:
            operation, args, kwargs = self.update_queue.get_nowait()
            self._execute_operation(operation, *args, **kwargs)
        except queue.Empty:
            pass
        finally:
            self.updating = False
            self._schedule_next_update()

    def _execute_operation(self, operation: str, *args, **kwargs) -> None:
        """Execute a text operation."""
        try:
            if operation == 'insert':
                self.text_widget.insert(*args, **kwargs)
            elif operation == 'delete':
                self.text_widget.delete(*args, **kwargs)
            elif operation == 'replace':
                start, end, text = args
                self.text_widget.delete(start, end)
                self.text_widget.insert(start, text, **kwargs)
            elif operation == 'configure':
                self.text_widget.configure(**kwargs)
            elif operation == 'see':
                self.text_widget.see(args[0])
            elif operation == 'mark_set':
                self.text_widget.mark_set(*args, **kwargs)
            elif operation == 'tag_add':
                self.text_widget.tag_add(*args, **kwargs)
            elif operation == 'tag_remove':
                self.text_widget.tag_remove(*args, **kwargs)
        except Exception as e:
            print(f"Text update error: {e}")


class UIRefreshManager:
    """Manages UI refresh operations to prevent excessive updates."""

    def __init__(self, root: tk.Tk, min_refresh_interval: float = 0.016):  # ~60 FPS
        self.root = root
        self.min_interval = min_refresh_interval
        self.last_refresh: float = 0
        self.pending_updates: Dict[str, Callable] = {}
        self.refresh_scheduled = False
        self._lock = threading.RLock()

    def schedule_refresh(self, key: str, update_func: Callable) -> None:
        """Schedule a UI refresh operation."""
        with self._lock:
            self.pending_updates[key] = update_func
            if not self.refresh_scheduled:
                self._schedule_refresh()

    def _schedule_refresh(self) -> None:
        """Schedule the next refresh."""
        current_time = time.time()
        time_since_last = current_time - self.last_refresh
        delay_ms = max(0, int((self.min_interval - time_since_last) * 1000))

        self.refresh_scheduled = True
        self.root.after(delay_ms, self._perform_refresh)

    def _perform_refresh(self) -> None:
        """Perform all pending refresh operations."""
        with self._lock:
            self.last_refresh = time.time()
            self.refresh_scheduled = False

            # Execute all pending updates
            for update_func in self.pending_updates.values():
                try:
                    update_func()
                except Exception as e:
                    print(f"UI refresh error: {e}")

            # Clear pending updates
            self.pending_updates.clear()


class OptimizedCanvas:
    """Optimized canvas with batched drawing operations."""

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.draw_queue: List[tuple] = []
        self.batch_size = 50
        self.processing = False
        self._lock = threading.RLock()

    def queue_draw_operation(self, operation: str, *args, **kwargs) -> None:
        """Queue a drawing operation."""
        with self._lock:
            self.draw_queue.append((operation, args, kwargs))
            if not self.processing and len(self.draw_queue) >= self.batch_size:
                self._schedule_batch_draw()

    def flush_draw_operations(self) -> None:
        """Flush all queued drawing operations."""
        with self._lock:
            if self.draw_queue and not self.processing:
                self._perform_batch_draw()

    def _schedule_batch_draw(self) -> None:
        """Schedule batch drawing."""
        if not self.processing:
            self.processing = True
            self.canvas.after(1, self._perform_batch_draw)

    def _perform_batch_draw(self) -> None:
        """Perform batched drawing operations."""
        with self._lock:
            try:
                operations = self.draw_queue[:self.batch_size]
                self.draw_queue = self.draw_queue[self.batch_size:]

                for operation, args, kwargs in operations:
                    try:
                        self._execute_draw_operation(operation, *args, **kwargs)
                    except Exception as e:
                        print(f"Draw operation error: {e}")

            finally:
                self.processing = False

                # Schedule next batch if more operations remain
                if self.draw_queue:
                    self._schedule_batch_draw()

    def _execute_draw_operation(self, operation: str, *args, **kwargs) -> None:
        """Execute a single drawing operation."""
        if operation == 'create_rectangle':
            self.canvas.create_rectangle(*args, **kwargs)
        elif operation == 'create_oval':
            self.canvas.create_oval(*args, **kwargs)
        elif operation == 'create_line':
            self.canvas.create_line(*args, **kwargs)
        elif operation == 'create_text':
            self.canvas.create_text(*args, **kwargs)
        elif operation == 'create_image':
            self.canvas.create_image(*args, **kwargs)
        elif operation == 'delete':
            self.canvas.delete(*args, **kwargs)
        elif operation == 'coords':
            self.canvas.coords(*args, **kwargs)
        elif operation == 'itemconfigure':
            self.canvas.itemconfigure(*args, **kwargs)
        elif operation == 'move':
            self.canvas.move(*args, **kwargs)


class EventBatcher:
    """Batches similar events to reduce processing overhead."""

    def __init__(self, root: tk.Tk, batch_window_ms: int = 100):
        self.root = root
        self.batch_window = batch_window_ms
        self.event_queues: Dict[str, List[tuple]] = {}
        self.timers: Dict[str, str] = {}
        self.handlers: Dict[str, Callable] = {}
        self._lock = threading.RLock()

    def register_handler(self, event_type: str, handler: Callable) -> None:
        """Register an event handler."""
        with self._lock:
            self.handlers[event_type] = handler

    def queue_event(self, event_type: str, *args, **kwargs) -> None:
        """Queue an event for batch processing."""
        with self._lock:
            if event_type not in self.event_queues:
                self.event_queues[event_type] = []

            self.event_queues[event_type].append((args, kwargs))

            # Schedule batch processing if not already scheduled
            if event_type not in self.timers:
                self.timers[event_type] = self.root.after(
                    self.batch_window,
                    partial(self._process_batch, event_type)
                )

    def _process_batch(self, event_type: str) -> None:
        """Process a batch of events."""
        with self._lock:
            if event_type in self.timers:
                del self.timers[event_type]

            if event_type in self.event_queues and event_type in self.handlers:
                events = self.event_queues[event_type]
                del self.event_queues[event_type]

                try:
                    self.handlers[event_type](events)
                except Exception as e:
                    print(f"Event batch processing error: {e}")


class GUIOptimizer:
    """Main GUI optimization coordinator."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.ui_thread_manager = UIThreadManager(root)
        self.refresh_manager = UIRefreshManager(root)
        self.event_batcher = EventBatcher(root)
        self.async_text_widgets: Dict[str, AsyncTextUpdate] = {}
        self.optimized_canvases: Dict[str, OptimizedCanvas] = {}

        # Performance monitoring
        self.update_count = 0
        self.last_stats_time = time.time()

    def start(self) -> None:
        """Start all GUI optimizations."""
        self.ui_thread_manager.start()

    def stop(self) -> None:
        """Stop all GUI optimizations."""
        self.ui_thread_manager.stop()

    def make_text_async(self, text_widget: tk.Text, name: str) -> AsyncTextUpdate:
        """Make a text widget use asynchronous updates."""
        async_text = AsyncTextUpdate(text_widget)
        self.async_text_widgets[name] = async_text
        return async_text

    def make_canvas_optimized(self, canvas: tk.Canvas, name: str) -> OptimizedCanvas:
        """Make a canvas use optimized drawing."""
        opt_canvas = OptimizedCanvas(canvas)
        self.optimized_canvases[name] = opt_canvas
        return opt_canvas

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get GUI performance statistics."""
        current_time = time.time()
        time_diff = current_time - self.last_stats_time
        updates_per_second = self.update_count / time_diff if time_diff > 0 else 0

        stats = {
            'updates_per_second': updates_per_second,
            'async_text_widgets': len(self.async_text_widgets),
            'optimized_canvases': len(self.optimized_canvases),
            'pending_ui_tasks': self.ui_thread_manager.task_queue.qsize(),
            'pending_refreshes': len(self.refresh_manager.pending_updates),
            'batched_events': sum(len(queue) for queue in self.event_batcher.event_queues.values())
        }

        # Reset counters
        self.update_count = 0
        self.last_stats_time = current_time

        return stats

    def optimize_for_performance(self) -> Dict[str, Any]:
        """Apply performance optimizations."""
        # Flush all pending operations
        for canvas in self.optimized_canvases.values():
            canvas.flush_draw_operations()

        for text_widget in self.async_text_widgets.values():
            # Force processing of remaining updates
            while not text_widget.update_queue.empty():
                text_widget._process_update()  # pylint: disable=protected-access

        return {
            'canvases_flushed': len(self.optimized_canvases),
            'text_widgets_synced': len(self.async_text_widgets),
            'ui_tasks_remaining': self.ui_thread_manager.task_queue.qsize()
        }


# Global GUI optimizer instance
gui_optimizer = None


def initialize_gui_optimizer(root: tk.Tk) -> GUIOptimizer:
    """Initialize the global GUI optimizer."""
    global gui_optimizer  # pylint: disable=global-statement
    if gui_optimizer is None:
        gui_optimizer = GUIOptimizer(root)
        gui_optimizer.start()
    return gui_optimizer


def get_gui_stats() -> Dict[str, Any]:
    """Get global GUI performance statistics."""
    if gui_optimizer:
        return gui_optimizer.get_performance_stats()
    return {'error': 'GUI optimizer not initialized'}
