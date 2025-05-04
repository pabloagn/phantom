#!/usr/bin/env python

# packages/phantom-visuals/src/phantom_visuals_v2/cli.py

"""Command line interface for phantom_visuals_v2."""

import glob
import multiprocessing
import os
import subprocess
import sys
import time
from typing import Any, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from phantom_visuals_v2.logger import console, get_logger, setup_logging

# Get logger
logger = get_logger()

# Create a lock for synchronizing console output in multiprocessing
output_lock = multiprocessing.Lock()


def process_image(
    input_path: str,
    output_path: str,
    effect: str = "vertical_cascade",
    config: Optional[str] = None,
    preset: Optional[str] = None,
    lock: Optional[Any] = None,
    verbose: bool = False,
) -> None:
    """Process an image with the specified effect.

    This is the core processing function that does the actual work.

    Args:
        input_path: Path to the input image
        output_path: Path to save the output image
        effect: Name of the effect to apply
        config: Path to configuration file
        preset: Name of the artistic preset
        lock: Optional lock for synchronizing console output
        verbose: Whether to enable verbose output
    """
    # Use lock if provided to synchronize console output
    if lock:
        lock.acquire()

    try:
        # Log the processing
        logger.info(f"Processing image: {input_path}")
        logger.info(f"Effect: {effect}")
        logger.info(f"Output: {output_path}")
        
        if verbose:
            logger.debug(f"Config: {config}")
            logger.debug(f"Preset: {preset}")
        
        # Show UI panel
        console.print(
            Panel.fit(
                f"Processing {input_path} with effect '{effect}'",
                title="Phantom Visuals V2",
                border_style="cyan",
            )
        )

        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Build command arguments
        cmd_args = [
            sys.executable,  # Use the current Python interpreter
            os.path.join(os.path.dirname(__file__), "run.py"),
            "-i", input_path,
            "-o", output_path,
        ]

        # Add optional arguments if provided
        if effect:
            cmd_args.extend(["-e", effect])

        if config:
            cmd_args.extend(["-c", config])

        if preset:
            cmd_args.extend(["-p", preset])
            
        # Add verbose flag if enabled
        if verbose:
            cmd_args.append("--verbose")

        # Log the command
        cmd_str = " ".join(cmd_args)
        logger.info(f"Running command: {cmd_str}")
        console.print(f"Running command: {cmd_str}", style="dim")

        # Run the actual processing command
        result = subprocess.run(
            cmd_args, 
            capture_output=True, 
            text=True, 
            check=False
        )

        # Handle the result
        if result.returncode != 0:
            logger.error(f"Error processing {input_path}")
            logger.error(f"Return code: {result.returncode}")
            logger.error(f"Error: {result.stderr}")
            
            console.print(
                f"Error processing {input_path}:", style="bold red"
            )
            console.print(f"Return code: {result.returncode}", style="red")
            console.print(f"Error: {result.stderr}", style="red")
        else:
            # Verify output file exists
            if os.path.exists(output_path):
                logger.info(f"Output saved to {output_path}")
                console.print(f"Output saved to {output_path}", style="green")
            else:
                logger.warning(f"Command successful but output file {output_path} not found!")
                console.print(
                    f"Warning: Command successful but output file {output_path} not found!",
                    style="bold yellow",
                )
                
        # Log stdout if verbose
        if verbose and result.stdout:
            logger.debug("Process output:")
            for line in result.stdout.splitlines():
                logger.debug(f"  {line}")
    except Exception as e:
        logger.exception(f"Exception during image processing: {e}")
        console.print(f"Exception during processing: {e}", style="bold red")
    finally:
        # Make sure we always release the lock
        if lock:
            lock.release()


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    default="INFO",
    help="Set the logging level",
)
@click.option(
    "--log-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    help="Directory for log files",
)
@click.option(
    "--no-file-log",
    is_flag=True,
    help="Disable logging to file",
)
def cli(log_level: str, log_dir: Optional[str], no_file_log: bool) -> None:
    """Phantom Visuals V2 - Advanced visual processing toolkit."""
    # Setup logging
    setup_logging(
        log_level=log_level,
        log_dir=log_dir,
        log_to_file=not no_file_log,
    )


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.option(
    "--effect",
    "-e",
    default="vertical_cascade",
    help="Visual effect to apply",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.option(
    "--preset",
    "-p",
    help="Artistic preset name",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
def process(
    input_path: str,
    output_path: str,
    effect: str,
    config: Optional[str],
    preset: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """Process an image or video with the specified effect."""
    # Log command execution
    logger.info(f"Running 'process' command")
    logger.info(f"Input: {input_path}")
    logger.info(f"Output: {output_path}")
    
    # Call the actual processing function
    process_image(input_path, output_path, effect, config, preset, verbose=verbose)


# This function is used by the process pool
def _process_image_for_batch(args: dict[str, Any]) -> None:
    """Process a single image for batch processing.

    Args:
        args: Dictionary containing image path and processing parameters
    """
    image_path = args["image_path"]
    output_dir = args["output_dir"]
    effect = args["effect"]
    config = args["config"]
    preset = args["preset"]
    lock = args["lock"]
    counter = args["counter"]
    verbose = args["verbose"]

    # Update the counter to show progress
    with counter.get_lock():
        counter.value += 1

    basename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, basename)

    # Call the actual processing function directly with the lock
    process_image(
        input_path=image_path,
        output_path=output_path,
        effect=effect or "vertical_cascade",  # Default from config
        config=config,
        preset=preset,
        lock=lock,
        verbose=verbose,
    )


@cli.command()
@click.option(
    "--input",
    "-i",
    default="input",
    help="Input directory with images",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
)
@click.option(
    "--output",
    "-o",
    default="output",
    help="Output directory",
    type=click.Path(file_okay=False, dir_okay=True),
)
@click.option(
    "--config",
    "-c",
    default=None,
    help="Configuration file to use",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option("--effect", "-e", default=None, help="Specific effect to apply")
@click.option("--preset", "-p", default=None, help="Artistic preset name")
@click.option(
    "--variations",
    "-v",
    default=1,
    help="Number of variations to generate per image",
    type=int,
)
@click.option(
    "--parallel",
    "-j",
    default=multiprocessing.cpu_count(),
    help="Number of parallel processes",
    type=int,
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose output",
)
def batch(
    input: str,
    output: str,
    config: Optional[str],
    effect: Optional[str],
    preset: Optional[str],
    variations: int,
    parallel: int,
    verbose: bool,
) -> None:
    """Batch process multiple images with artistic portrait transformations."""
    # Log command execution
    logger.info(f"Running 'batch' command")
    logger.info(f"Input directory: {input}")
    logger.info(f"Output directory: {output}")
    logger.info(f"Effect: {effect or 'default'}")
    logger.info(f"Parallel processes: {parallel}")
    
    # Ensure output directory exists
    os.makedirs(output, exist_ok=True)

    # Find all images in input directory
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff"]
    images: list[str] = []

    for ext in image_extensions:
        images.extend(glob.glob(os.path.join(input, ext)))
        images.extend(glob.glob(os.path.join(input, ext.upper())))

    if not images:
        logger.error(f"No images found in {input}")
        console.print(f"No images found in {input}", style="bold red")
        return

    total_images = len(images)
    logger.info(f"Found {total_images} images to process")
    console.print(f"Found {total_images} images to process", style="bold green")

    # Log detailed image list if verbose
    if verbose:
        logger.debug("Image files to process:")
        for img in images:
            logger.debug(f"  {img}")

    # Create a shared lock for console output
    lock = multiprocessing.Manager().Lock()

    # Create a counter for tracking progress
    counter = multiprocessing.Value("i", 0)

    # Prepare arguments for each image
    process_args = [
        {
            "image_path": img_path,
            "output_dir": output,
            "effect": effect,
            "config": config,
            "preset": preset,
            "lock": lock,
            "counter": counter,
            "verbose": verbose,
        }
        for img_path in images
    ]

    # Setup progress display in the main process
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        TimeRemainingColumn(),
    ) as progress:
        # Add task for overall progress
        task = progress.add_task(
            f"[cyan]Processing {total_images} images...", total=total_images
        )

        # Process images in parallel
        with multiprocessing.Pool(processes=parallel) as pool:
            # Start the pool processing
            result = pool.map_async(_process_image_for_batch, process_args)

            # Update progress while processing
            while not result.ready():
                # Update from the shared counter
                current = counter.value
                progress.update(task, completed=current)
                time.sleep(0.1)

            # Make sure we show 100% at the end
            progress.update(task, completed=total_images)

    logger.info(f"Processing complete. Results saved to {output}")
    logger.info(f"Processed {total_images} images with effect '{effect or 'vertical_cascade'}'")
    
    console.print(f"Processing complete. Results saved to {output}", style="bold green")
    console.print(
        f"✅ Processed {total_images} images with effect '{effect or 'vertical_cascade'}'",
        style="bold green",
    )


if __name__ == "__main__":
    cli()
