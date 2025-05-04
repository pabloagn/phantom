#!/usr/bin/env python

# packages/phantom-visuals/src/phantom_visuals_v2/batch_process.py

"""Batch processing script for phantom_visuals_v2.

Processes multiple images with artistic portrait transformations.
"""

import glob
import multiprocessing
import os
import time
from typing import Any

import click
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from phantom_visuals_v2.cli import process_image

console = Console()


# This function is used by the process pool
def _process_image(args: dict[str, Any]) -> None:
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

    # Update the counter to show progress
    with counter.get_lock():
        counter.value += 1

    basename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, basename)

    # Call the process function with the lock for synchronized output
    process_image(
        input_path=image_path,
        output_path=output_path,
        effect=effect or "vertical_cascade",  # Default from config
        config=config,
        preset=preset,
        lock=lock,
    )


@click.command()
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
def batch_process(
    input: str,
    output: str,
    config: str | None,
    effect: str | None,
    preset: str | None,
    variations: int,
    parallel: int,
) -> None:
    """Batch process multiple images with artistic portrait transformations."""
    # Ensure output directory exists
    os.makedirs(output, exist_ok=True)

    # Find all images in input directory
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff"]
    images: list[str] = []

    for ext in image_extensions:
        images.extend(glob.glob(os.path.join(input, ext)))
        images.extend(glob.glob(os.path.join(input, ext.upper())))

    if not images:
        console.print(f"No images found in {input}", style="bold red")
        return

    total_images = len(images)
    console.print(f"Found {total_images} images to process", style="bold green")

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
            result = pool.map_async(_process_image, process_args)

            # Update progress while processing
            while not result.ready():
                # Update from the shared counter
                current = counter.value
                progress.update(task, completed=current)
                time.sleep(0.1)

            # Make sure we show 100% at the end
            progress.update(task, completed=total_images)

    console.print(f"Processing complete. Results saved to {output}", style="bold green")
    console.print(
        f"✅ Processed {total_images} images with effect '{effect or 'vertical_cascade'}'",
        style="bold green",
    )


if __name__ == "__main__":
    batch_process()
