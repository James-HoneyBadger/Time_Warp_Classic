#!/usr/bin/env python3
"""
Memory management and optimization for Time_Warp_Classic.

This module provides memory optimization features including:
- Memory pool management
- Object reuse
- Memory monitoring
- Resource cleanup
"""

import gc
import weakref
import threading
from typing import Dict, List, Any, Optional, Set, Callable
from collections import defaultdict
import sys


class MemoryPool:
    """Memory pool for reusing objects to reduce allocation overhead."""

    def __init__(self, object_type: type, max_size: int = 100):
        self.object_type = object_type
        self.max_size = max_size
        self.pool: List[Any] = []
        self._lock = threading.RLock()

    def acquire(self) -> Any:
        """Get an object from the pool or create a new one."""
        with self._lock:
            if self.pool:
                return self.pool.pop()
            else:
                return self.object_type()

    def release(self, obj: Any) -> None:
        """Return an object to the pool for reuse."""
        with self._lock:
            if len(self.pool) < self.max_size and isinstance(obj, self.object_type):
                # Reset object state if possible
                if hasattr(obj, 'reset'):
                    try:
                        obj.reset()
                    except Exception:
                        pass  # Ignore reset errors
                self.pool.append(obj)

    def clear(self) -> None:
        """Clear all objects from the pool."""
        with self._lock:
            self.pool.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        with self._lock:
            return {
                'object_type': self.object_type.__name__,
                'current_size': len(self.pool),
                'max_size': self.max_size,
                'utilization': len(self.pool) / self.max_size
            }


class ObjectPoolManager:
    """Manager for multiple memory pools."""

    def __init__(self):
        self.pools: Dict[type, MemoryPool] = {}
        self._lock = threading.RLock()

    def get_pool(self, object_type: type, max_size: int = 100) -> MemoryPool:
        """Get or create a memory pool for the given type."""
        with self._lock:
            if object_type not in self.pools:
                self.pools[object_type] = MemoryPool(object_type, max_size)
            return self.pools[object_type]

    def acquire(self, object_type: type) -> Any:
        """Acquire an object from the appropriate pool."""
        return self.get_pool(object_type).acquire()

    def release(self, obj: Any) -> None:
        """Release an object back to its pool."""
        obj_type = type(obj)
        if obj_type in self.pools:
            self.pools[obj_type].release(obj)

    def clear_all(self) -> None:
        """Clear all memory pools."""
        with self._lock:
            for pool in self.pools.values():
                pool.clear()

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all pools."""
        with self._lock:
            return {pool.object_type.__name__: pool.get_stats() for pool in self.pools.values()}


class WeakReferenceManager:
    """Manager for weak references to prevent memory leaks."""

    def __init__(self):
        self.references: Dict[str, Set[weakref.ref]] = defaultdict(set)
        self._lock = threading.RLock()

    def add_reference(self, category: str, obj: Any) -> None:
        """Add a weak reference to an object."""
        with self._lock:
            ref = weakref.ref(obj, lambda r: self._remove_reference(category, r))
            self.references[category].add(ref)

    def _remove_reference(self, category: str, ref: weakref.ref) -> None:
        """Remove a dead weak reference."""
        with self._lock:
            self.references[category].discard(ref)

    def cleanup_dead_references(self, category: Optional[str] = None) -> int:
        """Clean up dead references and return count removed."""
        with self._lock:
            if category:
                categories = [category]
            else:
                categories = list(self.references.keys())

            removed = 0
            for cat in categories:
                alive_refs = set()
                for ref in self.references[cat]:
                    if ref() is not None:
                        alive_refs.add(ref)
                    else:
                        removed += 1
                self.references[cat] = alive_refs

            return removed

    def get_stats(self) -> Dict[str, Any]:
        """Get reference statistics."""
        with self._lock:
            stats = {}
            for category, refs in self.references.items():
                alive = sum(1 for ref in refs if ref() is not None)
                dead = len(refs) - alive
                stats[category] = {
                    'total': len(refs),
                    'alive': alive,
                    'dead': dead
                }
            return stats


class MemoryMonitor:
    """Memory usage monitoring and alerting."""

    def __init__(self, warning_threshold_mb: float = 100.0, critical_threshold_mb: float = 200.0):
        self.warning_threshold = warning_threshold_mb * 1024 * 1024
        self.critical_threshold = critical_threshold_mb * 1024 * 1024
        self.history: List[Dict[str, Any]] = []
        self.max_history_size = 100
        self._lock = threading.RLock()

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage."""
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()

            usage = {
                'rss': memory_info.rss,
                'vms': memory_info.vms,
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'gc_objects': len(gc.get_objects()),
                'timestamp': __import__('time').time()
            }

            # Add to history
            with self._lock:
                self.history.append(usage)
                if len(self.history) > self.max_history_size:
                    self.history.pop(0)

            return usage

        except ImportError:
            return {
                'gc_objects': len(gc.get_objects()),
                'note': 'psutil not available for detailed memory stats',
                'timestamp': __import__('time').time()
            }

    def check_thresholds(self) -> Dict[str, Any]:
        """Check if memory usage exceeds thresholds."""
        usage = self.get_memory_usage()
        rss = usage.get('rss', 0)

        alerts = []
        if rss > self.critical_threshold:
            alerts.append('CRITICAL')
        elif rss > self.warning_threshold:
            alerts.append('WARNING')

        return {
            'current_usage_mb': usage.get('rss_mb', 0),
            'warning_threshold_mb': self.warning_threshold / 1024 / 1024,
            'critical_threshold_mb': self.critical_threshold / 1024 / 1024,
            'alerts': alerts,
            'status': 'CRITICAL' if 'CRITICAL' in alerts else 'WARNING' if 'WARNING' in alerts else 'NORMAL'
        }

    def get_memory_history(self) -> List[Dict[str, Any]]:
        """Get memory usage history."""
        with self._lock:
            return self.history.copy()

    def get_peak_usage(self) -> Dict[str, Any]:
        """Get peak memory usage from history."""
        with self._lock:
            if not self.history:
                return {}

            peak_rss = max((h.get('rss', 0) for h in self.history), default=0)
            peak_vms = max((h.get('vms', 0) for h in self.history), default=0)

            return {
                'peak_rss_mb': peak_rss / 1024 / 1024,
                'peak_vms_mb': peak_vms / 1024 / 1024,
                'current_rss_mb': self.history[-1].get('rss_mb', 0) if self.history else 0,
                'current_vms_mb': self.history[-1].get('vms_mb', 0) if self.history else 0
            }


class ResourceManager:
    """Central resource management system."""

    def __init__(self):
        self.object_pools = ObjectPoolManager()
        self.weak_refs = WeakReferenceManager()
        self.memory_monitor = MemoryMonitor()
        self.cleanup_callbacks: List[Callable] = []
        self._lock = threading.RLock()

    def register_cleanup_callback(self, callback: Callable) -> None:
        """Register a cleanup callback function."""
        with self._lock:
            self.cleanup_callbacks.append(callback)

    def cleanup_resources(self) -> Dict[str, Any]:
        """Perform comprehensive resource cleanup."""
        results = {
            'object_pools_cleared': False,
            'dead_references_cleaned': 0,
            'garbage_collected': 0,
            'callbacks_executed': 0,
            'errors': []
        }

        try:
            # Clear object pools
            self.object_pools.clear_all()
            results['object_pools_cleared'] = True
        except Exception as e:
            results['errors'].append(f"Pool cleanup error: {e}")

        try:
            # Clean up dead references
            results['dead_references_cleaned'] = self.weak_refs.cleanup_dead_references()
        except Exception as e:
            results['errors'].append(f"Reference cleanup error: {e}")

        try:
            # Force garbage collection
            before = len(gc.get_objects())
            gc.collect()
            after = len(gc.get_objects())
            results['garbage_collected'] = max(0, before - after)
        except Exception as e:
            results['errors'].append(f"GC error: {e}")

        try:
            # Execute cleanup callbacks
            for callback in self.cleanup_callbacks:
                try:
                    callback()
                    results['callbacks_executed'] += 1
                except Exception as e:
                    results['errors'].append(f"Callback error: {e}")
        except Exception as e:
            results['errors'].append(f"Callback execution error: {e}")

        return results

    def get_resource_stats(self) -> Dict[str, Any]:
        """Get comprehensive resource statistics."""
        return {
            'memory': self.memory_monitor.get_memory_usage(),
            'memory_thresholds': self.memory_monitor.check_thresholds(),
            'object_pools': self.object_pools.get_all_stats(),
            'weak_references': self.weak_refs.get_stats(),
            'cleanup_callbacks': len(self.cleanup_callbacks)
        }

    def optimize_memory(self) -> Dict[str, Any]:
        """Apply memory optimizations."""
        results = self.cleanup_resources()

        # Additional optimizations
        try:
            # Clear any cached bytecode
            import sys
            if hasattr(sys, '_clear_type_cache'):
                sys._clear_type_cache()
                results['type_cache_cleared'] = True
            else:
                results['type_cache_cleared'] = False
        except Exception as e:
            results['errors'].append(f"Type cache clear error: {e}")
            results['type_cache_cleared'] = False

        return results


# Global resource manager instance
resource_manager = ResourceManager()

def get_memory_stats() -> Dict[str, Any]:
    """Get global memory statistics."""
    return resource_manager.get_resource_stats()

def cleanup_all_resources() -> Dict[str, Any]:
    """Global resource cleanup function."""
    return resource_manager.cleanup_resources()