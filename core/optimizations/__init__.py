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
    'get_gui_stats'
]

__version__ = '1.3.0'
