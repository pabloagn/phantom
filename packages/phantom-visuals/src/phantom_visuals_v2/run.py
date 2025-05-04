#!/usr/bin/env python

# packages/phantom-visuals/src/phantom_visuals_v2/run.py

"""Core run script for phantom_visuals_v2.

This script implements the image processing functionality for the Phantom Visuals V2 package.
It applies artistic effects to input images based on specified parameters.
"""

import argparse
import os
import sys
import traceback
from typing import Any, cast

import cv2
import numpy as np
import yaml
from rich.console import Console

console = Console()

# Try to import the advanced pipeline, but provide fallbacks if not available
ADVANCED_PIPELINE_AVAILABLE = False
try:
    from omegaconf import OmegaConf

    from phantom_visuals_v2.processors.core.pipeline import TransformationPipeline
    ADVANCED_PIPELINE_AVAILABLE = True
except ImportError as e:
    console.print(f"Advanced pipeline not available: {e}. Using fallback processing.", style="yellow")


def process_image(
    input_path: str,
    output_path: str,
    effect: str = "vertical_cascade",
    config_path: str | None = None,
    preset: str | None = None,
) -> bool:
    """Process a single image with artistic effects.

    Args:
        input_path: Path to the input image
        output_path: Path to save the output image
        effect: Name of the effect to apply
        config_path: Path to the configuration file
        preset: Optional preset name to use

    Returns:
        bool: True if processing was successful, False otherwise
    """
    try:
        # Load configuration
        config = load_config(config_path)

        # Load the input image
        img = cv2.imread(input_path)
        if img is None:
            console.print(f"Error: Could not load image {input_path}", style="bold red")
            return False

        # Convert to RGB for processing
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        console.print(f"Applying effect '{effect}' to {input_path}")

        # Process the image using the advanced pipeline if available
        if ADVANCED_PIPELINE_AVAILABLE:
            try:
                # Set primary effect in config
                if effect and "effects" in config:
                    config["effects"]["primary_effect"] = effect

                # Convert to OmegaConf for attribute access
                conf = OmegaConf.create(config)

                # Initialize the transformation pipeline
                pipeline = TransformationPipeline(conf)

                # Apply the transformation
                processed_result = pipeline.transform(img_rgb)

                # Handle both possible return types (image or tuple with intermediates)
                if isinstance(processed_result, tuple):
                    processed_img = processed_result[0]  # Extract just the image
                else:
                    processed_img = processed_result

            except Exception as e:
                console.print(f"Advanced pipeline failed: {e}", style="yellow")
                console.print("Falling back to basic effects processing")
                # Fall back to basic processing
                processed_img = apply_basic_effect(img_rgb, effect, config.get("effects", {}).get(effect, {}))
        else:
            # Use basic processing if the advanced pipeline is not available
            effect_config = get_effect_config(config, effect)
            processed_img = apply_basic_effect(img_rgb, effect, effect_config)

        # Convert back to BGR for saving
        output_img = cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Save the processed image
        cv2.imwrite(output_path, output_img)

        console.print(f"Saved processed image to {output_path}", style="green")
        return True

    except Exception as e:
        console.print(f"Error processing image: {e!s}", style="bold red")
        console.print(traceback.format_exc())
        return False


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load configuration from file.

    Args:
        config_path: Path to configuration file

    Returns:
        Dict containing configuration settings
    """
    # Default config path
    if config_path is None:
        config_path = os.path.join(
            os.path.dirname(__file__), "config", "default_config.yaml"
        )

    try:
        with open(config_path) as f:
            result = yaml.safe_load(f)
            return cast(dict[str, Any], result or {})
    except Exception as e:
        console.print(f"Error loading config: {e!s}", style="bold red")
        console.print("Using built-in defaults instead")
        return {}


def get_effect_config(config: dict[str, Any], effect_name: str) -> dict[str, Any]:
    """Get configuration for the specified effect.

    Args:
        config: Full configuration dictionary
        effect_name: Name of the effect

    Returns:
        Dict containing effect-specific configuration
    """
    # Get effect configuration from the config
    effects_config = config.get("effects", {})

    # Get the specific effect's configuration
    effect_config = effects_config.get(effect_name, {})

    return cast(dict[str, Any], effect_config)


def apply_basic_effect(
    img: np.ndarray, effect_name: str, effect_config: dict[str, Any]
) -> np.ndarray:
    """Apply a basic effect to the image when the advanced pipeline is not available.

    Args:
        img: Input image as a numpy array
        effect_name: Name of the effect to apply
        effect_config: Configuration for the effect

    Returns:
        Processed image as a numpy array
    """
    # This function provides basic fallback effects
    if effect_name == "vertical_cascade":
        return apply_vertical_cascade(img, effect_config)
    if effect_name == "horizontal_smear":
        return apply_horizontal_smear(img, effect_config)
    if effect_name == "data_glitch":
        return apply_data_glitch(img, effect_config)

    # Default to a simple effect
    console.print(f"Warning: Unknown effect '{effect_name}'. Using default effect.")
    return apply_vertical_cascade(img, effect_config)


def apply_vertical_cascade(img: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    """Apply vertical cascade effect.

    Args:
        img: Input image as a numpy array
        config: Effect configuration

    Returns:
        Processed image
    """
    # Get configuration parameters (with defaults)
    line_density = config.get("line_density", 100)
    line_thickness = config.get("line_thickness", 1)
    line_variation = config.get("line_variation", 0.3)

    # Create a copy of the input image
    result = img.copy()

    height, width = img.shape[:2]

    # Apply a simple vertical line effect
    for i in range(0, width, max(1, width // line_density)):
        thickness = max(
            1, int(line_thickness * (1 + np.random.randn() * line_variation))
        )
        color = np.random.randint(0, 256, 3)
        cv2.line(result, (i, 0), (i, height), color.tolist(), thickness)

    return result


def apply_horizontal_smear(img: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    """Apply horizontal smear effect.

    Args:
        img: Input image as a numpy array
        config: Effect configuration

    Returns:
        Processed image
    """
    # Get configuration parameters (with defaults)
    smear_strength = config.get("smear_strength", 0.8)
    direction_coherence = config.get("direction_coherence", 0.7)

    # Create output image
    result = img.copy()

    # Simple horizontal blur
    kernel_size = int(30 * smear_strength)
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure odd kernel size

    kernel_size = max(1, kernel_size)

    # Apply horizontal blur
    result = cv2.GaussianBlur(result, (kernel_size, 1), 0)

    # Blend with original based on direction coherence
    result = cv2.addWeighted(
        img, 1 - direction_coherence, result, direction_coherence, 0
    )

    return result


def apply_data_glitch(img: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    """Apply data glitch effect.

    Args:
        img: Input image as a numpy array
        config: Effect configuration

    Returns:
        Processed image
    """
    # Get configuration parameters (with defaults)
    glitch_density = config.get("glitch_density", 0.7)
    glitch_size = config.get("glitch_size", 0.1)
    horizontal_shift = config.get("horizontal_shift", 0.2)

    # Create output image
    result = img.copy()

    height, width = img.shape[:2]

    # Number of glitches
    num_glitches = int(height * glitch_density / 10)

    # Apply glitches
    for _ in range(num_glitches):
        # Random glitch position
        y = np.random.randint(0, height)
        h = max(1, int(height * glitch_size * np.random.random()))

        # Make sure we don't go out of bounds
        if y + h >= height:
            h = height - y - 1

        if h <= 0:
            continue

        # Extract a slice of the image
        slice_img = result[y : y + h, :].copy()

        # Randomly shift the slice horizontally
        shift = int(width * horizontal_shift * (np.random.random() * 2 - 1))

        if shift != 0:
            # Roll the slice horizontally
            slice_img = np.roll(slice_img, shift, axis=1)

            # Replace the original slice
            result[y : y + h, :] = slice_img

    return result


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Phantom Visuals V2 Processing Script")

    parser.add_argument("-i", "--input", required=True, help="Input image path")
    parser.add_argument("-o", "--output", required=True, help="Output image path")
    parser.add_argument(
        "-e", "--effect", default="vertical_cascade", help="Effect to apply"
    )
    parser.add_argument("-c", "--config", help="Path to configuration file")
    parser.add_argument("-p", "--preset", help="Preset name to use")

    args = parser.parse_args()

    # Process the image
    success = process_image(
        args.input, args.output, args.effect, args.config, args.preset
    )

    # Return appropriate exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
