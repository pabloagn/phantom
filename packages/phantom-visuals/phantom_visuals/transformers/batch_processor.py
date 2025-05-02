# packages/phantom-visuals/phantom_visuals/transformers/batch_processor.py

"""Batch processor for applying multiple styles to images.

This module provides utilities for batch processing images with multiple
style variants, making it easy to compare different visual treatments.
"""

import glob
import os
from pathlib import Path
from typing import Optional, Union

from phantom_visuals.core.config import (
    ColorScheme,
    Configuration,
    EffectParameters,
    OutputFormat,
    StyleVariant,
)
from phantom_visuals.transformers.abstract import AbstractComposer
from phantom_visuals.transformers.author import AuthorTransformer
from phantom_visuals.utils.logging import get_logger, log_processing_step, log_success

# Get logger
logger = get_logger()


class StyleExplorer:
    """Explorer for applying multiple styles to images.

    This class provides methods for applying all available styles
    or a subset of styles to input images, enabling visual exploration
    of different transformations.
    """

    def __init__(
        self,
        base_config: Optional[Configuration] = None,
        output_dir: Union[str, Path] = "output/styles",
    ):
        """Initialize the style explorer.

        Args:
            base_config: Base configuration to use for all transformations
            output_dir: Directory to save style explorations
        """
        self.base_config = base_config or Configuration()
        self.output_dir = Path(output_dir)

    def explore_author_styles(
        self,
        input_path: Union[str, Path],
        styles: Optional[list[str]] = None,
        color_schemes: Optional[list[str]] = None,
        intensity: float = 0.75,
        output_format: str = "png",
        create_comparison: bool = True,
    ) -> dict[str, list[Path]]:
        """Apply multiple styles to an author image.

        Args:
            input_path: Path to the input image or directory of images
            styles: List of styles to apply (if None, apply all styles)
            color_schemes: List of color schemes to apply (if None, use default)
            intensity: Effect intensity for all styles (0.0-1.0)
            output_format: Output file format (png, jpeg, webp, tiff)
            create_comparison: Whether to create a comparison grid

        Returns:
            Dictionary of style names and their output paths
        """
        # Validate input path
        input_paths = self._get_input_paths(input_path)
        if not input_paths:
            raise ValueError(f"No valid images found at {input_path}")

        # Get styles to apply
        style_variants = self._get_style_variants(styles)

        # Get color schemes to apply
        color_scheme_variants = self._get_color_schemes(color_schemes)

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Dictionary to store results
        results: dict[str, list[Path]] = {}

        # Process each input image
        for img_path in input_paths:
            log_processing_step(
                logger,
                "Processing Image",
                f"Applying {len(style_variants) * len(color_scheme_variants)} style variations to {img_path}",
            )

            # Create directory for this image
            img_name = Path(img_path).stem
            img_output_dir = self.output_dir / img_name
            os.makedirs(img_output_dir, exist_ok=True)

            # Process each style
            for style_name, style_value in style_variants.items():
                # Process each color scheme
                for scheme_name, scheme_value in color_scheme_variants.items():
                    # Create a unique configuration for this combination
                    params = EffectParameters(
                        intensity=intensity,
                        blur_radius=self.base_config.effect_params.blur_radius,
                        distortion=self.base_config.effect_params.distortion,
                        noise_level=self.base_config.effect_params.noise_level,
                        grain=self.base_config.effect_params.grain,
                        vignette=self.base_config.effect_params.vignette,
                        seed=self.base_config.effect_params.seed,
                    )

                    config = Configuration(
                        style_variant=StyleVariant(style_value),
                        color_scheme=ColorScheme(scheme_value),
                        output_format=OutputFormat(output_format),
                        effect_params=params,
                    )

                    # Create output filename
                    if len(color_scheme_variants) > 1:
                        # Include color scheme in the filename if multiple schemes
                        style_key = f"{style_name.lower()}_{scheme_name.lower()}"
                        output_filename = f"{img_name}_{style_name.lower()}_{scheme_name.lower()}.{output_format}"
                    else:
                        # Just use style name if only one color scheme
                        style_key = style_name.lower()
                        output_filename = (
                            f"{img_name}_{style_name.lower()}.{output_format}"
                        )

                    output_path = img_output_dir / output_filename

                    # Apply the transformation
                    log_processing_step(
                        logger,
                        f"Applying Style: {style_name}",
                        f"Color Scheme: {scheme_name}, Output: {output_path}",
                    )

                    # Create transformer and process the image
                    transformer = AuthorTransformer(config)
                    result_path = transformer.transform(img_path, output_path)

                    # Store the result
                    if style_key not in results:
                        results[style_key] = []
                    results[style_key].append(result_path)

            # Log completion for this image
            log_success(
                logger,
                f"Completed style exploration for {img_name}",
                {
                    "input": img_path,
                    "output_directory": str(img_output_dir),
                    "styles_applied": len(style_variants) * len(color_scheme_variants),
                },
            )

        return results

    def explore_abstract_styles(
        self,
        width: int = 1200,
        height: int = 1600,
        styles: Optional[list[str]] = None,
        color_schemes: Optional[list[str]] = None,
        intensity: float = 0.75,
        output_format: str = "png",
        create_comparison: bool = True,
    ) -> dict[str, list[Path]]:
        """Create abstract compositions with multiple styles.

        Args:
            width: Width of compositions in pixels
            height: Height of compositions in pixels
            styles: List of styles to apply (if None, apply all styles)
            color_schemes: List of color schemes to apply (if None, use default)
            intensity: Effect intensity for all styles (0.0-1.0)
            output_format: Output file format (png, jpeg, webp, tiff)
            create_comparison: Whether to create a comparison grid

        Returns:
            Dictionary of style names and their output paths
        """
        # Get styles to apply
        style_variants = self._get_style_variants(styles)

        # Get color schemes to apply
        color_scheme_variants = self._get_color_schemes(color_schemes)

        # Create output directory
        abstract_dir = self.output_dir / "abstract"
        os.makedirs(abstract_dir, exist_ok=True)

        # Dictionary to store results
        results: dict[str, list[Path]] = {}

        log_processing_step(
            logger,
            "Creating Abstract Compositions",
            f"Generating {len(style_variants) * len(color_scheme_variants)} style variations",
        )

        # Process each style
        for style_name, style_value in style_variants.items():
            # Process each color scheme
            for scheme_name, scheme_value in color_scheme_variants.items():
                # Create a unique configuration for this combination
                params = EffectParameters(
                    intensity=intensity,
                    blur_radius=self.base_config.effect_params.blur_radius,
                    distortion=self.base_config.effect_params.distortion,
                    noise_level=self.base_config.effect_params.noise_level,
                    grain=self.base_config.effect_params.grain,
                    vignette=self.base_config.effect_params.vignette,
                    seed=self.base_config.effect_params.seed,
                )

                config = Configuration(
                    style_variant=StyleVariant(style_value),
                    color_scheme=ColorScheme(scheme_value),
                    output_format=OutputFormat(output_format),
                    effect_params=params,
                )

                # Create output filename
                if len(color_scheme_variants) > 1:
                    # Include color scheme in the filename if multiple schemes
                    style_key = f"{style_name.lower()}_{scheme_name.lower()}"
                    output_filename = f"abstract_{style_name.lower()}_{scheme_name.lower()}.{output_format}"
                else:
                    # Just use style name if only one color scheme
                    style_key = style_name.lower()
                    output_filename = f"abstract_{style_name.lower()}.{output_format}"

                output_path = abstract_dir / output_filename

                # Apply the transformation
                log_processing_step(
                    logger,
                    f"Creating Abstract with Style: {style_name}",
                    f"Color Scheme: {scheme_name}, Output: {output_path}",
                )

                # Create composer and generate the composition
                composer = AbstractComposer(config)
                result_path = composer.create_composition(width, height, output_path)

                # Store the result
                if style_key not in results:
                    results[style_key] = []
                results[style_key].append(result_path)

        # Log completion
        log_success(
            logger,
            "Completed abstract style exploration",
            {
                "output_directory": str(abstract_dir),
                "compositions_created": len(style_variants)
                * len(color_scheme_variants),
            },
        )

        return results

    def _get_input_paths(self, input_path: Union[str, Path]) -> list[Path]:
        """Get list of valid input image paths."""
        input_path = Path(input_path)

        # If directory or glob pattern, get all matching files
        if "*" in str(input_path) or "?" in str(input_path):
            # Glob pattern
            return [Path(p) for p in glob.glob(str(input_path))]
        elif input_path.is_dir():
            # Directory - get all image files
            image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif"]
            image_files = []
            for ext in image_extensions:
                image_files.extend(input_path.glob(f"*{ext}"))
                image_files.extend(input_path.glob(f"*{ext.upper()}"))
            return image_files
        elif input_path.is_file():
            # Single file
            return [input_path]
        else:
            return []

    def _get_style_variants(self, styles: Optional[list[str]] = None) -> dict[str, str]:
        """Get dictionary of style names and values."""
        all_styles = {style.name: style.value for style in StyleVariant}

        if styles is None or len(styles) == 0:
            # Return all styles if None or empty list
            return all_styles
        else:
            # Filter to selected styles, handling case-insensitivity
            selected_styles = {}
            styles_upper = [s.upper() for s in styles]

            for name, value in all_styles.items():
                if name.upper() in styles_upper or value.lower() in [
                    s.lower() for s in styles
                ]:
                    selected_styles[name] = value

            return selected_styles

    def _get_color_schemes(self, schemes: Optional[list[str]] = None) -> dict[str, str]:
        """Get dictionary of color scheme names and values."""
        all_schemes = {scheme.name: scheme.value for scheme in ColorScheme}

        if schemes is None:
            # Return just the default color scheme
            return {"PHANTOM_CORE": "phantom_core"}
        elif schemes == ["all"]:
            # Return all color schemes
            return all_schemes
        else:
            # Filter to selected schemes, handling case-insensitivity
            selected_schemes = {}
            schemes_upper = [s.upper() for s in schemes]

            for name, value in all_schemes.items():
                if name.upper() in schemes_upper or value.lower() in [
                    s.lower() for s in schemes
                ]:
                    selected_schemes[name] = value

            return selected_schemes
