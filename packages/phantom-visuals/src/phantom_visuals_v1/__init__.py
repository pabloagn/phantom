# packages/phantom-visuals/phantom_visuals/__init__.py

"""Phantom Visuals - Advanced image manipulation for the Phantom ecosystem.

This package provides tools for transforming images with artistic effects,
creating abstract compositions, and maintaining a consistent visual language
for the Phantom brand.
"""

__version__ = "0.1.0"

from phantom_visuals_v1.core import Configuration, StyleEngine
from phantom_visuals_v1.effects import EffectChain
from phantom_visuals_v1.transformers import (
    AbstractComposer,
    AuthorTransformer,
    DigitalArtist,
)

__all__ = [
    "StyleEngine",
    "Configuration",
    "AuthorTransformer",
    "AbstractComposer",
    "DigitalArtist",
    "EffectChain",
]
