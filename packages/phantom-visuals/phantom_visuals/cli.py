# packages/phantom-visuals/phantom_visuals/cli.py

"""Command-line interface for Phantom Visuals.

This module provides a powerful CLI for applying image transformations
and creating abstract compositions using the Phantom Visuals toolkit.
"""

import json
import os
from pathlib import Path
from typing import List, Optional

import typer
from rich import box
from rich.panel import Panel
from rich.table import Table

from phantom_visuals.core.config import (
    ColorScheme,
    Configuration,
    EffectParameters,
    OutputFormat,
    StyleVariant,
)
from phantom_visuals.transformers import (
    AbstractComposer,
    AuthorTransformer,
    StyleExplorer,
)
from phantom_visuals.utils.logging import (
    console,
    create_progress_bar,
    log_cli_command,
    log_config,
    log_error,
    log_processing_step,
    log_success,
    setup_logging,
)

app = typer.Typer(
    name="phantom-visuals",
    help="A powerful image transformation and generation toolkit for the Phantom ecosystem.",
    add_completion=False,
)

logger = setup_logging()


@app.command("transform")
def transform_images(
    input_path: str = typer.Argument(
        ...,
        help="Path to the input image or directory (glob pattern supported)",
    ),
    output_path: str = typer.Option(
        "output",
        "--output",
        "-o",
        help="Path to save the transformed image(s)",
    ),
    style: str = typer.Option(
        "phantom",
        "--style",
        "-s",
        help="Style variant to apply",
    ),
    intensity: float = typer.Option(
        0.75,
        "--intensity",
        "-i",
        min=0.0,
        max=1.0,
        help="Effect intensity (0.0-1.0)",
    ),
    blur: float = typer.Option(
        0.0,
        "--blur",
        "-b",
        min=0.0,
        max=50.0,
        help="Blur radius (0.0-50.0)",
    ),
    distortion: float = typer.Option(
        0.0,
        "--distortion",
        "-d",
        min=0.0,
        max=1.0,
        help="Distortion amount (0.0-1.0)",
    ),
    noise: float = typer.Option(
        0.0,
        "--noise",
        "-n",
        min=0.0,
        max=1.0,
        help="Noise level (0.0-1.0)",
    ),
    grain: float = typer.Option(
        0.0,
        "--grain",
        "-g",
        min=0.0,
        max=1.0,
        help="Film grain amount (0.0-1.0)",
    ),
    vignette: float = typer.Option(
        0.0,
        "--vignette",
        "-v",
        min=0.0,
        max=1.0,
        help="Vignette amount (0.0-1.0)",
    ),
    color_scheme: str = typer.Option(
        "phantom_core",
        "--color-scheme",
        "-c",
        help="Color scheme to use",
    ),
    output_format: str = typer.Option(
        "png",
        "--format",
        "-f",
        help="Output file format (png, jpeg, webp, tiff)",
    ),
    seed: Optional[int] = typer.Option(
        None,
        "--seed",
        help="Random seed for reproducible results",
    ),
    save_config: Optional[str] = typer.Option(
        None,
        "--save-config",
        help="Save the current configuration to a JSON file",
    ),
    load_config: Optional[str] = typer.Option(
        None,
        "--load-config",
        help="Load configuration from a JSON file",
    ),
    batch: bool = typer.Option(
        False,
        "--batch",
        "-B",
        help="Process multiple images using a glob pattern",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ),
) -> None:
    """Transform images with Phantom Visuals effects."""
    try:
        # Update logging level if specified
        if log_level:
            logger.setLevel(log_level.upper())

        # Log command execution
        command_args = {
            "input_path": input_path,
            "output_path": output_path,
            "style": style,
            "intensity": intensity,
            "blur": blur,
            "distortion": distortion,
            "noise": noise,
            "grain": grain,
            "vignette": vignette,
            "color_scheme": color_scheme,
            "output_format": output_format,
            "seed": seed,
            "batch": batch,
            "save_config": save_config,
            "load_config": load_config,
        }
        log_cli_command(logger, "transform", command_args)

        # Load configuration from file if specified
        if load_config:
            log_processing_step(
                logger, "Loading Configuration", f"From file: {load_config}"
            )
            config = Configuration.from_file(load_config)
        else:
            # Create configuration with provided parameters
            log_processing_step(
                logger, "Creating Configuration", "Using command line parameters"
            )
            params = EffectParameters(
                intensity=intensity,
                blur_radius=blur,
                distortion=distortion,
                noise_level=noise,
                grain=grain,
                vignette=vignette,
                seed=seed,
            )

            config = Configuration(
                style_variant=StyleVariant(style),
                color_scheme=ColorScheme(color_scheme),
                output_format=OutputFormat(output_format),
                effect_params=params,
            )

        # Log configuration
        log_config(logger, json.loads(config.model_dump_json()))

        # Save configuration if requested
        if save_config:
            log_processing_step(
                logger, "Saving Configuration", f"To file: {save_config}"
            )
            config.to_file(save_config)
            log_success(logger, "Configuration saved", {"file": save_config})

        # Create the transformer
        log_processing_step(logger, "Initializing Transformer", f"Style: {style}")
        transformer = AuthorTransformer(config)

        # Process the image(s)
        if batch:
            # Check if output is a directory
            output_dir = Path(output_path)
            if not output_dir.is_dir():
                os.makedirs(output_dir, exist_ok=True)

            # Process batch of images
            log_processing_step(
                logger, "Starting Batch Processing", f"Glob pattern: {input_path}"
            )

            # Create a progress bar
            progress = create_progress_bar("Processing batch", transient=False)

            with progress:
                task = progress.add_task(
                    "[phantom]Transforming images...[/phantom]", total=None
                )
                results = transformer.batch_transform(input_path, output_dir, style)
                progress.update(task, completed=len(results), total=len(results))

            # Log success
            log_success(
                logger,
                "Batch processing complete",
                {
                    "processed": len(results),
                    "output_directory": str(output_dir),
                    "style": style,
                },
            )
        else:
            # Process a single image
            log_processing_step(logger, "Processing Image", f"Input: {input_path}")

            # Determine output path
            if os.path.isdir(output_path):
                input_filename = os.path.basename(input_path)
                base_name = os.path.splitext(input_filename)[0]
                output_file = os.path.join(
                    output_path, f"{base_name}.{config.output_format.value}"
                )
            else:
                output_file = output_path

            # Make sure the output directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

            # Create a progress bar for processing
            progress = create_progress_bar("Processing image")

            with progress:
                task = progress.add_task(
                    "[phantom]Transforming image...[/phantom]", total=100
                )

                # Update progress to simulate processing steps
                progress.update(
                    task,
                    advance=25,
                    description="[phantom]Analyzing image...[/phantom]",
                )

                # Start the transformation
                result_path = transformer.transform(input_path, output_file, style)

                # Complete the progress
                progress.update(
                    task,
                    completed=100,
                    description="[phantom]Transformation complete![/phantom]",
                )

            # Log success
            log_success(
                logger,
                "Image processed successfully",
                {"input": input_path, "output": str(result_path), "style": style},
            )

    except Exception as e:
        log_error(logger, e)
        raise typer.Exit(code=1)


@app.command("create")
def create_composition(
    output_path: str = typer.Option(
        "output/abstract.png",
        "--output",
        "-o",
        help="Path to save the generated composition",
    ),
    width: int = typer.Option(
        1200,
        "--width",
        "-W",
        min=100,
        help="Width of the composition in pixels",
    ),
    height: int = typer.Option(
        1600,
        "--height",
        "-H",
        min=100,
        help="Height of the composition in pixels",
    ),
    style: str = typer.Option(
        "abstract",
        "--style",
        "-s",
        help="Style variant to apply",
    ),
    intensity: float = typer.Option(
        0.75,
        "--intensity",
        "-i",
        min=0.0,
        max=1.0,
        help="Effect intensity (0.0-1.0)",
    ),
    blur: float = typer.Option(
        5.0,
        "--blur",
        "-b",
        min=0.0,
        max=50.0,
        help="Blur radius (0.0-50.0)",
    ),
    distortion: float = typer.Option(
        0.3,
        "--distortion",
        "-d",
        min=0.0,
        max=1.0,
        help="Distortion amount (0.0-1.0)",
    ),
    noise: float = typer.Option(
        0.2,
        "--noise",
        "-n",
        min=0.0,
        max=1.0,
        help="Noise level (0.0-1.0)",
    ),
    grain: float = typer.Option(
        0.3,
        "--grain",
        "-g",
        min=0.0,
        max=1.0,
        help="Film grain amount (0.0-1.0)",
    ),
    vignette: float = typer.Option(
        0.4,
        "--vignette",
        "-v",
        min=0.0,
        max=1.0,
        help="Vignette amount (0.0-1.0)",
    ),
    color_scheme: str = typer.Option(
        "phantom_core",
        "--color-scheme",
        "-c",
        help="Color scheme to use",
    ),
    output_format: str = typer.Option(
        "png",
        "--format",
        "-f",
        help="Output file format (png, jpeg, webp, tiff)",
    ),
    seed: Optional[int] = typer.Option(
        None,
        "--seed",
        help="Random seed for reproducible results",
    ),
    load_config: Optional[str] = typer.Option(
        None,
        "--load-config",
        help="Load configuration from a JSON file",
    ),
    count: int = typer.Option(
        1,
        "--count",
        min=1,
        help="Number of compositions to generate",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ),
) -> None:
    """Create abstract art compositions."""
    try:
        # Update logging level if specified
        if log_level:
            logger.setLevel(log_level.upper())

        # Log command execution
        command_args = {
            "output_path": output_path,
            "width": width,
            "height": height,
            "style": style,
            "intensity": intensity,
            "blur": blur,
            "distortion": distortion,
            "noise": noise,
            "grain": grain,
            "vignette": vignette,
            "color_scheme": color_scheme,
            "output_format": output_format,
            "seed": seed,
            "load_config": load_config,
            "count": count,
        }
        log_cli_command(logger, "create", command_args)

        # Load configuration from file if specified
        if load_config:
            log_processing_step(
                logger, "Loading Configuration", f"From file: {load_config}"
            )
            config = Configuration.from_file(load_config)
        else:
            # Create configuration with provided parameters
            log_processing_step(
                logger, "Creating Configuration", "Using command line parameters"
            )
            params = EffectParameters(
                intensity=intensity,
                blur_radius=blur,
                distortion=distortion,
                noise_level=noise,
                grain=grain,
                vignette=vignette,
                seed=seed,
            )

            config = Configuration(
                style_variant=StyleVariant(style),
                color_scheme=ColorScheme(color_scheme),
                output_format=OutputFormat(output_format),
                effect_params=params,
            )

        # Log configuration
        log_config(logger, json.loads(config.model_dump_json()))

        # Create the composer
        log_processing_step(logger, "Initializing Composer", f"Style: {style}")
        composer = AbstractComposer(config)

        # Generate multiple compositions if requested
        if count > 1:
            # Process multiple compositions
            results = []

            # Create progress bar for multiple compositions
            progress = create_progress_bar(
                f"Creating {count} compositions", total=count
            )

            with progress:
                # Create a task for tracking progress
                task = progress.add_task(
                    "[phantom]Generating compositions...[/phantom]", total=count
                )

                for i in range(count):
                    # Ensure unique seed for each composition if seed is provided
                    if seed is not None:
                        current_seed = seed + i
                        # Update seed in config for each iteration
                        config.effect_params.seed = current_seed
                        composer = AbstractComposer(config)

                    # Generate unique filename
                    output_file = Path(output_path)
                    if i > 0:
                        # Add index to filename for multiple compositions
                        stem = output_file.stem
                        output_file = output_file.with_stem(f"{stem}_{i+1}")

                    # Make sure the output directory exists
                    os.makedirs(
                        os.path.dirname(os.path.abspath(output_file)), exist_ok=True
                    )

                    # Update task description and advance progress
                    progress.update(
                        task,
                        description=f"[phantom]Generating composition {i+1} of {count}...[/phantom]",
                        advance=1,
                    )

                    # Create the composition
                    result_path = composer.create_composition(
                        width, height, output_file, style
                    )
                    results.append(result_path)

            # Log success
            log_success(
                logger,
                f"Generated {count} compositions",
                {
                    "width": width,
                    "height": height,
                    "style": style,
                    "output_directory": os.path.dirname(os.path.abspath(output_file)),
                },
            )

        else:
            # Create a single composition
            log_processing_step(
                logger,
                "Creating Composition",
                f"Size: {width}x{height}, Style: {style}",
            )

            # Make sure the output directory exists
            output_file = Path(output_path)
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

            # Create a progress bar for the generation
            progress = create_progress_bar("Creating composition")

            with progress:
                task = progress.add_task(
                    "[phantom]Generating artwork...[/phantom]", total=100
                )

                # Update progress to simulate processing steps
                progress.update(
                    task,
                    advance=30,
                    description="[phantom]Building base canvas...[/phantom]",
                )
                progress.update(
                    task,
                    advance=30,
                    description="[phantom]Applying effects...[/phantom]",
                )

                # Create the composition
                result_path = composer.create_composition(
                    width, height, output_file, style
                )

                # Complete the progress
                progress.update(
                    task,
                    completed=100,
                    description="[phantom]Composition complete![/phantom]",
                )

            # Log success
            log_success(
                logger,
                "Composition created successfully",
                {
                    "width": width,
                    "height": height,
                    "style": style,
                    "output": str(result_path),
                },
            )

    except Exception as e:
        log_error(logger, e)
        raise typer.Exit(code=1)


@app.command("styles")
def list_styles(
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ),
) -> None:
    """List available style variants."""
    try:
        # Update logging level if specified
        if log_level:
            logger.setLevel(log_level.upper())

        # Log command execution
        log_cli_command(logger, "styles", {"log_level": log_level})

        # Get all available styles
        styles = {style.name: style.value for style in StyleVariant}

        # Create a table for the styles
        table = Table(
            title="[header]Available Style Variants[/header]",
            box=box.ROUNDED,
            border_style="cyan",
            title_style="header",
            header_style="subheader",
            row_styles=["", "dim"],
            highlight=True,
            expand=False,
            show_header=True,
        )

        table.add_column("Style", style="highlight")
        table.add_column("Value", style="value")
        table.add_column("Description", style="parameter")

        # Style descriptions
        descriptions = {
            "MINIMAL": "Clean, minimalist aesthetic with subtle effects",
            "DUOTONE": "Two-color palette with high contrast",
            "ABSTRACT": "Complex abstract patterns and textures",
            "ETHEREAL": "Dreamy, foggy, atmospheric style",
            "MODERNIST": "Bold shapes and clean lines inspired by modernism",
            "PHANTOM": "Default Phantom style with eerie, ghostly aesthetics",
            "GOTHIC": "Dark, moody with high contrast and vignette",
            "GLITCH": "Digital artifacts and distortion effects",
            "SYMMETRICAL": "Balanced, mirrored composition",
            "MINIMAL_ORGANIC": "Minimal style with organic, flowing elements",
            "ABSTRACT_WILD": "Highly abstract with unpredictable elements",
            "GLITCH_REFINED": "Sophisticated glitch effects with artistic color manipulation",
            "ETHEREAL_ORGANIC": "Dreamy atmospheric style with organic patterns",
            "MODERNIST_ORGANIC": "Modernist style with organic textures and flows",
            "PHANTOM_ENHANCED": "Enhanced version of the phantom style with richer effects",
            "GOTHIC_DISTORTED": "Gothic style with distortion and mirror effects",
            "CONTOUR": "Contour map effect with elegant line work",
            "WAVE": "Wave-based patterns with harmonic oscillations",
            # Mathematical styles
            "FRACTAL": "Mathematical fractal patterns based on the Mandelbrot set",
            "FOURIER": "Frequency domain transformations with wave analysis",
            "WAVE_FUNCTION": "Quantum wave function patterns and interference effects",
            "STATISTICAL": "Statistical transformations with local normalization",
            # New style variations
            "GOTHIC_SUBTLE": "Gothic style with subtle, pervasive distortion effects",
            "PHANTOM_SPECTRAL": "Enhanced phantasmagoric effects with spectral quality",
            "GLITCH_BALANCED": "Balanced glitch effects preserving image integrity",
            "SPECTRAL_VEIL": "Ghostly veil overlaying the image with transparency",
            "GHOST_TRAILS": "Subtle ghosting and trailing effects throughout the image",
            # Long exposure style
            "PHANTOM_FLOW": "Organic long-exposure effect with flowing phantasmagoric movements and film grain",
        }

        # Add rows for each style
        for name, value in styles.items():
            desc = descriptions.get(name, "Custom style variant")
            table.add_row(name.lower(), value, desc)

        # Display the table
        console.print(table)

        # Add some usage examples
        console.print(
            Panel(
                "[parameter]Example usage:[/parameter]\n"
                "[dim]phantom-visuals transform input.jpg --style phantom[/dim]\n"
                "[dim]phantom-visuals create --style abstract --width 1200 --height 1600[/dim]",
                title="[phantom]Style Usage Examples[/phantom]",
                border_style="cyan",
                box=box.ROUNDED,
                expand=False,
            )
        )

    except Exception as e:
        log_error(logger, e)
        raise typer.Exit(code=1)


@app.command("colors")
def list_colors(
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ),
) -> None:
    """List available color schemes."""
    try:
        # Update logging level if specified
        if log_level:
            logger.setLevel(log_level.upper())

        # Log command execution
        log_cli_command(logger, "colors", {"log_level": log_level})

        # Get all available color schemes
        colors = {scheme.name: scheme.value for scheme in ColorScheme}

        # Create a table for the color schemes
        table = Table(
            title="[header]Available Color Schemes[/header]",
            box=box.ROUNDED,
            border_style="cyan",
            title_style="header",
            header_style="subheader",
            row_styles=["", "dim"],
            highlight=True,
            expand=False,
            show_header=True,
        )

        table.add_column("Scheme", style="highlight")
        table.add_column("Value", style="value")
        table.add_column("Description", style="parameter")

        # Color scheme descriptions
        descriptions = {
            "PHANTOM_CORE": "Default Phantom color palette with rich purples and blues",
            "DARK_CONTRAST": "High contrast dark palette with dramatic lighting",
            "ETHEREAL": "Soft, dreamy pastel colors with low saturation",
            "MONOCHROME": "Black and white with grayscale tones",
            "NEON": "Bright, vibrant colors with high saturation",
            "DUOTONE_BLUE": "Blue duotone palette with varying shades",
            "DUOTONE_RED": "Red duotone palette with varying shades",
            "VINTAGE": "Warm, faded colors reminiscent of old photographs",
            "CYBERPUNK": "Neon colors on dark background with high contrast",
            "GOTHIC": "Dark, muted colors with deep shadows",
        }

        # Add rows for each color scheme
        for name, value in colors.items():
            desc = descriptions.get(name, "Custom color scheme")
            table.add_row(name.lower(), value, desc)

        # Display the table
        console.print(table)

        # Add some usage examples
        console.print(
            Panel(
                "[parameter]Example usage:[/parameter]\n"
                "[dim]phantom-visuals transform input.jpg --color-scheme dark_contrast[/dim]\n"
                "[dim]phantom-visuals create --color-scheme ethereal --style abstract[/dim]",
                title="[phantom]Color Scheme Usage Examples[/phantom]",
                border_style="cyan",
                box=box.ROUNDED,
                expand=False,
            )
        )

    except Exception as e:
        log_error(logger, e)
        raise typer.Exit(code=1)


@app.command("config")
def config_tool(
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Configuration name/filename",
    ),
    output: str = typer.Option(
        "configs",
        "--output",
        "-o",
        help="Directory to save the configuration",
    ),
    style: str = typer.Option(
        "phantom",
        "--style",
        "-s",
        help="Style variant to apply",
    ),
    intensity: float = typer.Option(
        0.75,
        "--intensity",
        "-i",
        min=0.0,
        max=1.0,
        help="Effect intensity (0.0-1.0)",
    ),
    blur: float = typer.Option(
        0.0,
        "--blur",
        "-b",
        min=0.0,
        max=50.0,
        help="Blur radius (0.0-50.0)",
    ),
    distortion: float = typer.Option(
        0.0,
        "--distortion",
        "-d",
        min=0.0,
        max=1.0,
        help="Distortion amount (0.0-1.0)",
    ),
    noise: float = typer.Option(
        0.0,
        "--noise",
        "-n",
        min=0.0,
        max=1.0,
        help="Noise level (0.0-1.0)",
    ),
    grain: float = typer.Option(
        0.0,
        "--grain",
        "-g",
        min=0.0,
        max=1.0,
        help="Film grain amount (0.0-1.0)",
    ),
    vignette: float = typer.Option(
        0.0,
        "--vignette",
        "-v",
        min=0.0,
        max=1.0,
        help="Vignette amount (0.0-1.0)",
    ),
    color_scheme: str = typer.Option(
        "phantom_core",
        "--color-scheme",
        "-c",
        help="Color scheme to use",
    ),
    output_format: str = typer.Option(
        "png",
        "--format",
        "-f",
        help="Output file format (png, jpeg, webp, tiff)",
    ),
    seed: Optional[int] = typer.Option(
        None,
        "--seed",
        help="Random seed for reproducible results",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ),
) -> None:
    """Create and manage configurations."""
    try:
        # Update logging level if specified
        if log_level:
            logger.setLevel(log_level.upper())

        # Log command execution
        command_args = {
            "name": name,
            "output": output,
            "style": style,
            "intensity": intensity,
            "blur": blur,
            "distortion": distortion,
            "noise": noise,
            "grain": grain,
            "vignette": vignette,
            "color_scheme": color_scheme,
            "output_format": output_format,
            "seed": seed,
        }
        log_cli_command(logger, "config", command_args)

        # Create configuration with provided parameters
        log_processing_step(
            logger,
            "Creating Configuration",
            f"Style: {style}, Color Scheme: {color_scheme}",
        )
        params = EffectParameters(
            intensity=intensity,
            blur_radius=blur,
            distortion=distortion,
            noise_level=noise,
            grain=grain,
            vignette=vignette,
            seed=seed,
        )

        config = Configuration(
            style_variant=StyleVariant(style),
            color_scheme=ColorScheme(color_scheme),
            output_format=OutputFormat(output_format),
            effect_params=params,
        )

        # Log configuration
        log_config(logger, json.loads(config.model_dump_json()))

        # Determine the filename
        if name is None:
            name = f"{style}_{color_scheme}"

        # Ensure the filename has .json extension
        if not name.lower().endswith(".json"):
            name = f"{name}.json"

        # Create the output directory if it doesn't exist
        os.makedirs(output, exist_ok=True)
        config_path = os.path.join(output, name)

        # Save the configuration
        log_processing_step(logger, "Saving Configuration", f"File: {config_path}")
        config.to_file(config_path)

        # Log success
        log_success(
            logger,
            "Configuration saved successfully",
            {"file": config_path, "style": style, "color_scheme": color_scheme},
        )

        # Add usage example
        console.print(
            Panel(
                f"[parameter]Use this configuration with:[/parameter]\n"
                f"[dim]phantom-visuals transform input.jpg --load-config {config_path}[/dim]\n"
                f"[dim]phantom-visuals create --load-config {config_path}[/dim]",
                title="[phantom]Configuration Usage Examples[/phantom]",
                border_style="cyan",
                box=box.ROUNDED,
                expand=False,
            )
        )

    except Exception as e:
        log_error(logger, e)
        raise typer.Exit(code=1)


@app.command("explore")
def explore_styles(
    input_path: str = typer.Argument(
        ...,
        help="Path to the input image or directory (glob pattern supported)",
    ),
    output_dir: str = typer.Option(
        "output/explore",  # Changed default slightly
        "--output",
        "-o",
        help="Directory to save style explorations or flavor results",
    ),
    styles: List[str] = typer.Option(  # Use List from typing
        None,  # Default changed to None (process all available for the mode)
        "--style",
        "-s",
        help="Styles to apply (omit for all available styles in the selected mode)",
    ),
    flavor_config_path: Optional[str] = typer.Option(  # <--- NEW OPTION
        None,
        "--flavor-config",
        "-fc",
        help="Path to TOML file defining specific 'best flavor' parameters for styles. If set, other parameter flags are ignored.",
        exists=True,  # Typer checks if file exists
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    # --- Parameters below are PRIMARILY for the default exploration mode ---
    # --- They are ignored if --flavor-config is used ---
    color_schemes: List[str] = typer.Option(  # Use List from typing
        None,
        "--color-scheme",
        "-c",
        help="Color schemes for default exploration (ignored if --flavor-config is used; use 'all' for all schemes)",
    ),
    intensity: float = typer.Option(
        0.75, "--intensity", "-i", help="Intensity (ignored if --flavor-config used)"
    ),
    blur: float = typer.Option(
        0.0, "--blur", "-b", help="Blur radius (ignored if --flavor-config used)"
    ),
    distortion: float = typer.Option(
        0.0, "--distortion", "-d", help="Distortion (ignored if --flavor-config used)"
    ),
    noise: float = typer.Option(
        0.0, "--noise", "-n", help="Noise level (ignored if --flavor-config used)"
    ),
    grain: float = typer.Option(
        0.0, "--grain", "-g", help="Grain amount (ignored if --flavor-config used)"
    ),
    vignette: float = typer.Option(
        0.0,
        "--vignette",
        "-v",
        help="Vignette amount (ignored if --flavor-config used)",
    ),
    # Seed is still relevant for both modes potentially
    seed: Optional[int] = typer.Option(
        None, "--seed", help="Global random seed override"
    ),
    output_format: str = typer.Option(
        "png", "--format", "-f", help="Output file format (png, jpeg, webp, tiff)"
    ),
    # Abstract mode - less relevant for flavors, keep for original mode
    abstract: bool = typer.Option(
        False,
        "--abstract",
        "-a",
        help="Create abstract compositions (default exploration mode only)",
    ),
    width: int = typer.Option(
        1200, "--width", "-W", help="Width for abstract compositions"
    ),
    height: int = typer.Option(
        1600, "--height", "-H", help="Height for abstract compositions"
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Logging level"),
) -> None:
    """Explore style variations using default mode OR predefined 'best flavor' parameters."""
    try:
        if log_level:
            logger.setLevel(log_level.upper())

        # --- Differentiate between modes ---
        if flavor_config_path:
            # --- BEST FLAVOR MODE ---
            log_processing_step(logger, "Mode Selected", "Best Flavor Comparison")
            command_args = {
                "input_path": input_path,
                "output_dir": output_dir,
                "flavor_config_path": flavor_config_path,
                "styles": styles if styles else "ALL (from config)",
                "output_format": output_format,
                # Seed is still relevant potentially if not set in TOML
                "seed_override": seed,
            }
            log_cli_command(logger, "explore (flavor mode)", command_args)

            # Instantiate explorer (base_config less important here, output_dir is crucial)
            # Output dir passed to run_best_flavors will be used directly
            explorer = StyleExplorer(output_dir=output_dir)  # Pass output dir here

            # Run the flavor comparison
            results = explorer.run_best_flavors(
                input_path=input_path,
                output_dir=output_dir,  # Pass the command line output dir
                parameter_config_path=flavor_config_path,
                styles_to_run=styles,  # Pass None or the list
                output_format=output_format,
                # Maybe allow overriding default color scheme via CLI too? For now, use default in method
            )

            # Simple summary for flavor mode
            if results:
                console.print(
                    f"\n[bold green]✓[/] Best Flavor processing complete. Results saved in: [cyan]{output_dir}[/]"
                )
                # Optionally list generated files/styles
                table = Table(title="Generated Flavors", box=box.MINIMAL_HEAVY_HEAD)
                table.add_column("Style Flavor", style="green")
                table.add_column("Output File", style="cyan")
                for style_key, out_path in results.items():
                    table.add_row(style_key, str(out_path))
                console.print(table)
            else:
                console.print(
                    "[yellow]No flavor images were generated (check logs for details).[/]"
                )

        else:
            # --- DEFAULT EXPLORATION MODE ---
            log_processing_step(logger, "Mode Selected", "Default Style Exploration")
            command_args = {
                "input_path": input_path,
                "output_dir": output_dir,
                "styles": styles if styles else "ALL",
                "color_schemes": color_schemes if color_schemes else "DEFAULT",
                "intensity": intensity,
                "blur": blur,
                "distortion": distortion,
                "noise": noise,
                "grain": grain,
                "vignette": vignette,
                "output_format": output_format,
                "seed": seed,
                "abstract": abstract,
                "width": width,
                "height": height,
            }
            log_cli_command(logger, "explore (default mode)", command_args)

            # Create base configuration using CLI parameters OR defaults
            params = EffectParameters(
                intensity=intensity,
                blur_radius=blur,
                distortion=distortion,
                noise_level=noise,
                grain=grain,
                vignette=vignette,
                seed=seed,
            )
            # Base config only used to pass defaults to explore methods now
            config = Configuration(
                effect_params=params, output_format=OutputFormat(output_format)
            )
            # Note: Default style/color in base config doesn't matter much here

            # Instantiate explorer, passing the base output dir for comparisons
            explorer = StyleExplorer(base_config=config, output_dir=output_dir)

            if abstract:
                # --- Abstract Exploration ---
                if not styles:
                    log_info(logger, "Generating abstract for all styles.")
                if not color_schemes:
                    log_info(logger, "Using default color scheme for abstract.")

                results = explorer.explore_abstract_styles(
                    width=width,
                    height=height,
                    styles=styles,
                    color_schemes=color_schemes,
                    # Pass relevant params if explore_abstract_styles uses them
                    intensity=intensity,
                    output_format=output_format,
                )
                summary_title = "Abstract Style Exploration Summary"
                output_location_msg = (
                    f"Open the images in {explorer.output_dir / 'abstract'} to compare."
                )

            else:
                # --- Author Image Exploration ---
                if not styles:
                    log_info(logger, "Exploring all styles on images.")
                if not color_schemes:
                    log_info(logger, "Using default color scheme for exploration.")

                # Call the original exploration method, passing overrides
                results = explorer.explore_author_styles(
                    input_path=input_path,
                    styles=styles,
                    color_schemes=color_schemes,
                    intensity=intensity,
                    blur_radius=blur,
                    distortion=distortion,
                    noise_level=noise,
                    grain=grain,
                    vignette=vignette,
                    seed=seed,
                    output_format=output_format,
                )
                summary_title = "Image Style Exploration Summary"
                # Output dir structure is now <output_dir>/<image_name>/<image>_<style>[_color].png
                output_location_msg = f"Open the subdirectories within {explorer.output_dir} to compare styles per image."

            # Display summary table (common to both abstract/author exploration)
            if results:
                style_table = Table(
                    title=f"[header]{summary_title}[/header]",
                    box=box.ROUNDED,
                    border_style="cyan",
                )
                style_table.add_column("Style Combination", style="highlight")
                style_table.add_column("Files Created / Last Output", style="value")
                for style_key, paths in results.items():
                    # Show count for author, just path for abstract? Or always last path?
                    display_val = (
                        f"{len(paths)} files" if isinstance(paths, list) else str(paths)
                    )
                    style_table.add_row(style_key, display_val)
                console.print(style_table)
                console.print(
                    Panel(
                        f"[dim]{output_location_msg}[/dim]",
                        title="[phantom]Next Steps[/phantom]",
                        border_style="cyan",
                    )
                )
            else:
                console.print("[yellow]No exploration images were generated.[/]")

    except Exception as e:
        log_error(
            logger, f"Error during explore command: {e}"
        )  # Show traceback for explore errors
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
