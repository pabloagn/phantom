# packages/phantom-visuals/phantom_visuals/core/engine.py

"""StyleEngine - The core processing engine for Phantom Visuals.

This module provides the foundation for all image transformations,
handling the loading, processing, and saving of images.
"""

from typing import Dict, List, Optional, Tuple, Union, Any, Callable
from pathlib import Path
import os
import random
import numpy as np
from PIL import Image

from phantom_visuals.core.config import Configuration, StyleVariant, ColorScheme
from phantom_visuals.core.palette import ColorPalette


class StyleEngine:
    """The main engine for applying style transformations to images.

    This class handles image loading, transformation pipeline management,
    and saving the processed results.
    """

    def __init__(self, config: Optional[Configuration] = None):
        """Initialize the style engine with the given configuration."""
        self.config = config or Configuration()
        self.palette = ColorPalette.from_scheme(self.config.color_scheme)
        self._transformations: List[Callable] = []

    def set_config(self, config: Configuration) -> "StyleEngine":
        """Update the engine configuration."""
        self.config = config
        self.palette = ColorPalette.from_scheme(config.color_scheme)
        return self

    def set_palette(self, palette: ColorPalette) -> "StyleEngine":
        """Set a custom color palette."""
        self.palette = palette
        return self

    def reset_transformations(self) -> "StyleEngine":
        """Clear all transformations in the pipeline."""
        self._transformations = []
        return self

    def add_transformation(self, transform_fn: Callable) -> "StyleEngine":
        """Add a transformation function to the pipeline."""
        self._transformations.append(transform_fn)
        return self

    def load_image(self, path: Union[str, Path]) -> np.ndarray:
        """Load an image from the given path and convert to a numpy array.

        Args:
            path: Path to the image file

        Returns:
            A numpy array representing the image in RGB format
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")

        image = Image.open(path).convert("RGB")
        return np.array(image)

    def save_image(self, image: np.ndarray, path: Union[str, Path]) -> Path:
        """Save a numpy array as an image.

        Args:
            image: Numpy array representing the image
            path: Path where the image should be saved

        Returns:
            Path where the image was saved
        """
        path = Path(path)
        os.makedirs(path.parent, exist_ok=True)

        # Convert the numpy array back to PIL Image
        img = Image.fromarray(image.astype(np.uint8))

        # Determine the format based on extension or configuration
        format_ext = path.suffix.lstrip(".").upper()
        if not format_ext:
            format_ext = self.config.output_format.value.upper()
            path = path.with_suffix(f".{self.config.output_format.value}")

        # Save with the appropriate quality
        img.save(
            path, format=format_ext, quality=self.config.output_quality, optimize=True
        )

        return path

    def process_image(self, image: np.ndarray) -> np.ndarray:
        """Apply all transformations in the pipeline to the image.

        Args:
            image: Numpy array representing the input image

        Returns:
            The processed image as a numpy array
        """
        # Set the random seed for reproducible results
        if self.config.effect_params.seed is not None:
            random.seed(self.config.effect_params.seed)
            np.random.seed(self.config.effect_params.seed)

        result = image.copy()

        # Apply each transformation in sequence
        for transform in self._transformations:
            result = transform(result, self.config, self.palette)

        return result

    def transform(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ) -> Path:
        """Load an image, apply all transformations, and save the result.

        Args:
            input_path: Path to the input image
            output_path: Path where the output should be saved

        Returns:
            The path where the transformed image was saved
        """
        image = self.load_image(input_path)
        processed = self.process_image(image)
        return self.save_image(processed, output_path)

    def batch_transform(
        self, input_paths: List[Union[str, Path]], output_dir: Union[str, Path]
    ) -> List[Path]:
        """Process multiple images and save them to the specified directory.

        Args:
            input_paths: List of paths to the input images
            output_dir: Directory where the processed images should be saved

        Returns:
            List of paths where the transformed images were saved
        """
        output_dir = Path(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        results = []
        for input_path in input_paths:
            input_path = Path(input_path)
            output_path = output_dir / input_path.name
            output_path = output_path.with_suffix(f".{self.config.output_format.value}")

            try:
                result_path = self.transform(input_path, output_path)
                results.append(result_path)
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

        return results
