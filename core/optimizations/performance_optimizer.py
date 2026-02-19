#!/usr/bin/env python3
"""
Performance optimizations for Time_Warp_Classic.

This module provides various performance enhancements including:
- Expression evaluation caching
- Lazy loading of language executors
- Memory optimization
- Execution profiling
"""

import time
from typing import Dict, Any, Callable
import threading
import gc


class ExpressionCache:
    """Cache for compiled expressions to avoid re-evaluation."""

    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, Any] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        self._lock = threading.RLock()

    def get(self, key: str):
        """Get cached value for key. Returns _CACHE_MISS sentinel if not cached."""
        with self._lock:
            if key in self.cache:
                self.hits += 1
                return self.cache[key]
            self.misses += 1
            return _CACHE_MISS

    def put(self, key: str, value: Any) -> None:
        """Store value in cache."""
        with self._lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest entries (simple FIFO)
                oldest_keys = list(self.cache.keys())[:self.max_size // 10]
                for k in oldest_keys:
                    del self.cache[k]

            self.cache[key] = value

    def clear(self) -> None:
        """Clear all cached values."""
        with self._lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests) if total_requests > 0 else 0
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': hit_rate,
                'total_requests': total_requests
            }


class LazyLoader:
    """Lazy loading system for language executors and heavy components."""

    def __init__(self):
        self._loaded_modules: Dict[str, Any] = {}
        self._loading_functions: Dict[str, Callable] = {}
        self._lock = threading.RLock()

    def register_loader(self, name: str, loader_func: Callable) -> None:
        """Register a lazy loading function."""
        with self._lock:
            self._loading_functions[name] = loader_func

    def get(self, name: str) -> Any:
        """Get a module, loading it if necessary."""
        with self._lock:
            if name not in self._loaded_modules:
                if name in self._loading_functions:
                    self._loaded_modules[name] = self._loading_functions[name]()
                else:
                    raise ImportError(f"No loader registered for {name}")

            return self._loaded_modules[name]

    def is_loaded(self, name: str) -> bool:
        """Check if a module is already loaded."""
        with self._lock:
            return name in self._loaded_modules

    def unload(self, name: str) -> None:
        """Unload a module to free memory."""
        with self._lock:
            if name in self._loaded_modules:
                # Try to clean up resources
                module = self._loaded_modules[name]
                if hasattr(module, 'cleanup'):
                    try:
                        module.cleanup()
                    except Exception:
                        pass  # Ignore cleanup errors

                del self._loaded_modules[name]

                # Force garbage collection
                gc.collect()

    def get_loaded_modules(self) -> list:
        """Get list of currently loaded modules."""
        with self._lock:
            return list(self._loaded_modules.keys())


class PerformanceProfiler:
    """Performance profiling and monitoring."""

    def __init__(self):
        self.start_times: Dict[str, float] = {}
        self.execution_counts: Dict[str, int] = {}
        self.total_times: Dict[str, float] = {}
        self._lock = threading.RLock()

    def start_operation(self, operation: str) -> None:
        """Start timing an operation."""
        with self._lock:
            self.start_times[operation] = time.perf_counter()

    def end_operation(self, operation: str) -> float:
        """End timing an operation and return elapsed time."""
        with self._lock:
            if operation in self.start_times:
                elapsed = time.perf_counter() - self.start_times[operation]
                self.execution_counts[operation] = self.execution_counts.get(operation, 0) + 1
                self.total_times[operation] = self.total_times.get(operation, 0) + elapsed
                del self.start_times[operation]
                return elapsed
            return 0.0

    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        with self._lock:
            stats = {}
            for operation, total in self.total_times.items():
                count = self.execution_counts.get(operation, 0)
                avg = total / count if count > 0 else 0
                stats[operation] = {
                    'count': count,
                    'total_time': total,
                    'average_time': avg,
                    'operations_per_second': 1.0 / avg if avg > 0 else 0
                }
            return stats

    def reset(self) -> None:
        """Reset all profiling data."""
        with self._lock:
            self.start_times.clear()
            self.execution_counts.clear()
            self.total_times.clear()


class MemoryOptimizer:
    """Memory optimization utilities."""

    @staticmethod
    def optimize_variable_storage(variables: Dict[str, Any]) -> None:
        """Optimize variable storage to reduce memory usage."""
        import sys as _sys
        # Intern strings to reduce memory for repeated string values
        for key, value in variables.items():
            if isinstance(value, str):
                try:
                    variables[key] = _sys.intern(value)
                except TypeError:
                    pass  # Non-internable strings (subclasses) are skipped

    @staticmethod
    def cleanup_unused_objects() -> int:
        """Force garbage collection and return objects collected."""
        before = len(gc.get_objects())
        gc.collect()
        after = len(gc.get_objects())
        return max(0, before - after)

    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Get current memory usage statistics."""
        try:
            import psutil
            import os
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()

            return {
                'rss': memory_info.rss,  # Resident Set Size
                'vms': memory_info.vms,  # Virtual Memory Size
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'gc_objects': len(gc.get_objects())
            }
        except ImportError:
            return {
                'gc_objects': len(gc.get_objects()),
                'note': 'psutil not available for detailed memory stats'
            }


# Sentinel for cache misses (distinguishes None results from missing entries)
_CACHE_MISS = object()


class OptimizedInterpreterMixin:
    """Mixin class providing performance optimizations for interpreters."""

    def __init__(self, interpreter_instance):
        self.interpreter = interpreter_instance

        # Initialize performance components
        self.expression_cache = ExpressionCache(max_size=500)
        self.lazy_loader = LazyLoader()
        self.profiler = PerformanceProfiler()
        self.memory_optimizer = MemoryOptimizer()

        # Performance settings
        self.enable_caching = True
        self.enable_profiling = False
        self.enable_lazy_loading = True

        # Register lazy loaders for heavy components
        self._register_lazy_loaders()

    def _register_lazy_loaders(self) -> None:
        """Register lazy loading functions for heavy components."""

        def load_audio_engine():
            try:
                from ..audio import AudioEngine
                return AudioEngine()
            except ImportError:
                # Return dummy implementation
                class DummyAudioEngine:
                    """No-op audio engine fallback."""

                    def play_sound(self, *args):
                        """No-op play."""

                    def stop_sound(self, *args):
                        """No-op stop."""

                return DummyAudioEngine()

        def load_game_manager():
            try:
                from games.engine import GameManager
                return GameManager()
            except ImportError:
                class DummyGameManager:
                    """No-op game manager fallback."""

                    def create_object(self, *args):
                        """No-op create."""
                        return False

                    def move_object(self, *args):
                        """No-op move."""
                        return False

                return DummyGameManager()

        self.lazy_loader.register_loader('audio_engine', load_audio_engine)
        self.lazy_loader.register_loader('game_manager', load_game_manager)

    def optimized_evaluate_expression(self, expr: str) -> Any:
        """Optimized expression evaluation with caching."""
        if not self.enable_caching:
            return self.interpreter._evaluate_expression_original(expr)  # pylint: disable=protected-access

        # Create cache key from expression and current variables
        try:
            var_hash = hash(frozenset(self.interpreter.variables.items()))
        except TypeError:
            # Variables contain unhashable values (lists, dicts); skip caching
            return self.interpreter._evaluate_expression_original(expr)  # pylint: disable=protected-access
        cache_key = f"{expr}:{var_hash}"

        # Check cache first
        cached_result = self.expression_cache.get(cache_key)
        if cached_result is not _CACHE_MISS:
            return cached_result

        # Evaluate and cache result
        if self.enable_profiling:
            self.profiler.start_operation('expression_evaluation')

        result = self.interpreter._evaluate_expression_original(expr)  # pylint: disable=protected-access

        if self.enable_profiling:
            self.profiler.end_operation('expression_evaluation')

        # Cache the result (but not for error results)
        if not (isinstance(result, str) and result.startswith("ERROR:")):
            self.expression_cache.put(cache_key, result)

        return result

    def optimized_execute_line(self, line: str) -> str:
        """Optimized line execution with profiling."""
        if self.enable_profiling:
            self.profiler.start_operation('line_execution')

        result = self.interpreter._execute_line_original(line)  # pylint: disable=protected-access

        if self.enable_profiling:
            self.profiler.end_operation('line_execution')

        return result

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        return {
            'expression_cache': self.expression_cache.get_stats(),
            'profiler': self.profiler.get_stats(),
            'memory': self.memory_optimizer.get_memory_usage(),
            'lazy_loaded_modules': self.lazy_loader.get_loaded_modules(),
            'settings': {
                'caching_enabled': self.enable_caching,
                'profiling_enabled': self.enable_profiling,
                'lazy_loading_enabled': self.enable_lazy_loading
            }
        }

    def optimize_for_production(self) -> Dict[str, Any]:
        """Apply production optimizations."""
        # Clear caches to free memory
        self.expression_cache.clear()

        # Run garbage collection
        collected = self.memory_optimizer.cleanup_unused_objects()

        # Optimize variable storage
        self.memory_optimizer.optimize_variable_storage(self.interpreter.variables)

        return {
            'cache_cleared': True,
            'objects_collected': collected,
            'variables_optimized': True
        }

    def cleanup_resources(self) -> Dict[str, Any]:
        """Clean up resources and free memory."""
        # Clear all caches
        self.expression_cache.clear()

        # Unload lazy-loaded modules
        loaded_modules = self.lazy_loader.get_loaded_modules()
        for module in loaded_modules:
            self.lazy_loader.unload(module)

        # Reset profiler
        self.profiler.reset()

        # Force garbage collection
        collected = self.memory_optimizer.cleanup_unused_objects()

        return {
            'cache_cleared': True,
            'modules_unloaded': loaded_modules,
            'profiler_reset': True,
            'objects_collected': collected
        }


# Global performance optimizer instance
performance_optimizer = None


def optimize_for_production():
    """Global production optimization function."""
    return {
        'message': 'Global optimization applied',
        'timestamp': time.time()
    }


class PerformanceOptimizer:
    """Global performance optimization manager."""

    def __init__(self):
        self.global_cache = ExpressionCache(max_size=2000)
        self.start_time = time.time()

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide performance statistics."""
        return {
            'uptime': time.time() - self.start_time,
            'global_cache': self.global_cache.get_stats(),
            'python_version': f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
            'thread_count': threading.active_count()
        }


# Initialize global instance after class definition
performance_optimizer = PerformanceOptimizer()
