# packages/phantom-visuals/phantom_visuals/effects/base.py

"""
Base classes for the effects system.

This module provides the foundation for chaining and composing different
image effects together.
"""

from typing import List, Callable, Dict, Any, Optional
import numpy as np

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.palette import ColorPalette


EffectFunction = Callable[[np.ndarray, Configuration, ColorPalette], np.ndarray]


class EffectChain:
    """
    A chainable collection of image effects.

    This class allows for a fluent interface to build up a sequence of
    image processing effects that can be applied to an image.
    """

    def __init__(self):
        """Initialize an empty effect chain."""
        self._effects: List[EffectFunction] = []

    def add(self, effect: EffectFunction) -> "EffectChain":
        """
        Add an effect to the chain.

        Args:
            effect: A function that takes an image array, config, and palette
                   and returns a processed image array

        Returns:
            The EffectChain instance for method chaining
        """
        self._effects.append(effect)
        return self

    def apply(self, image: np.ndarray, config: Configuration, palette: ColorPalette) -> np.ndarray:
        """
        Apply all effects in the chain to the image.

        Args:
            image: The input image as a numpy array
            config: The configuration object
            palette: The color palette to use

        Returns:
            The processed image as a numpy array
        """
        result = image.copy()
        for effect in self._effects:
            result = effect(result, config, palette)
        return result

    def reset(self) -> "EffectChain":
        """
        Remove all effects from the chain.

        Returns:
            The EffectChain instance for method chaining
        """
        self._effects = []
        return self

    def __call__(self, image: np.ndarray, config: Configuration, palette: ColorPalette) -> np.ndarray:
        """
        Apply the effect chain to an image when the chain is called as a function.

        Args:
            image: The input image as a numpy array
            config: The configuration object
            palette: The color palette to use

        Returns:
            The processed image as a numpy array
        """
        return self.apply(image, config, palette)


def compose_effects(*effects: EffectFunction) -> EffectFunction:
    """
    Compose multiple effect functions into a single function.

    Args:
        *effects: One or more effect functions to compose

    Returns:
        A single effect function that applies all the input effects in sequence
    """
    def composed_effect(image: np.ndarray, config: Configuration, palette: ColorPalette) -> np.ndarray:
        result = image.copy()
        for effect in effects:
            result = effect(result, config, palette)
        return result

    return composed_effect
