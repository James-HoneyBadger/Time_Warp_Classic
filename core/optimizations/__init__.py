#!/usr/bin/env python3
"""
Performance optimizations package for Time_Warp_Classic.

This package provides various performance enhancements including:
- Expression caching and lazy loading
- Memory management and optimization
- GUI responsiveness improvements
- Resource cleanup and monitoring
"""

from .performance_optimizer import (
    ExpressionCache,
    LazyLoader,
    PerformanceProfiler,
    MemoryOptimizer,
    OptimizedInterpreterMixin,
    performance_optimizer,
    optimize_for_production
)

from .memory_manager import (
    MemoryPool,
    ObjectPoolManager,
    WeakReferenceManager,
    MemoryMonitor,
    ResourceManager,
    resource_manager,
    get_memory_stats,
    cleanup_all_resources
)

try:
    from .gui_optimizer import (
        UIThreadManager,
        AsyncTextUpdate,
        UIRefreshManager,
        OptimizedCanvas,
        EventBatcher,
        GUIOptimizer,
        initialize_gui_optimizer,
        get_gui_stats
    )
    GUI_OPTIMIZER_AVAILABLE = True
except ImportError:  # pragma: no cover - headless installs without Tk
    # The web UI and exported runners have no widgets; the rest of the
    # optimisations still work, so keep the package importable.
    GUI_OPTIMIZER_AVAILABLE = False
    UIThreadManager = AsyncTextUpdate = UIRefreshManager = None
    OptimizedCanvas = EventBatcher = GUIOptimizer = None

    def initialize_gui_optimizer(*_args, **_kwargs):
        return None

    def get_gui_stats():
        return {}

__all__ = [
    # Performance optimizer
    'ExpressionCache',
    'LazyLoader',
    'PerformanceProfiler',
    'MemoryOptimizer',
    'OptimizedInterpreterMixin',
    'performance_optimizer',
    'optimize_for_production',

    # Memory manager
    'MemoryPool',
    'ObjectPoolManager',
    'WeakReferenceManager',
    'MemoryMonitor',
    'ResourceManager',
    'resource_manager',
    'get_memory_stats',
    'cleanup_all_resources',

    # GUI optimizer
    'UIThreadManager',
    'AsyncTextUpdate',
    'UIRefreshManager',
    'OptimizedCanvas',
    'EventBatcher',
    'GUIOptimizer',
    'initialize_gui_optimizer',
    'get_gui_stats',
    'GUI_OPTIMIZER_AVAILABLE',
]

__version__ = '1.5.0'
