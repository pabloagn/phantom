# packages/phantom-visuals/phantom_visuals/core/__init__.py

"""Core components for the Phantom Visuals system.

This module provides the foundational classes for configuration,
style management, and image processing.
"""

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.engine import StyleEngine
from phantom_visuals.core.palette import ColorPalette

__all__ = ["Configuration", "StyleEngine", "ColorPalette"]
