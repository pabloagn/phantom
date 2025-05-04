# Phantom Visuals V2

Enhanced visual processing toolkit for creating artistic visual effects.

## Package Structure

The package is organized as follows:

```text
phantom_visuals_v2/
│
├── __init__.py         # Package initialization
├── cli.py              # Command-line interface
├── batch_process.py    # Batch processing utility
│
├── config/             # Configuration files and utilities
│   ├── __init__.py
│   └── default_config.yaml
│
├── processors/         # Processing components
│   ├── __init__.py
│   │
│   ├── core/           # Core functionality and abstractions
│   │   └── __init__.py
│   │
│   ├── analysis/       # Image analysis components
│   │   └── __init__.py
│   │
│   ├── flow/           # Optical flow generation
│   │   └── __init__.py
│   │
│   ├── material/       # Material simulation
│   │   └── __init__.py
│   │
│   ├── composition/    # Composition and blending
│   │   └── __init__.py
│   │
│   ├── temporal/       # Temporal coherence processing
│   │   └── __init__.py
│   │
│   ├── aesthetics/     # Aesthetic refinement
│   │   └── __init__.py
│   │
│   └── effects/        # Visual effects
│       └── __init__.py
```

## Usage

```python
# Example usage of the package
from phantom_visuals_v2 import cli

# Run the CLI
cli.cli()

# Batch process images
cli.batch()
```

## Command Line Usage

```bash
# Process a single image with the default effect
phantom-visuals process input.jpg output.jpg

# Process with a specific effect
phantom-visuals process input.jpg output.jpg --effect horizontal_smear

# Process with a custom configuration
phantom-visuals process input.jpg output.jpg --config my_config.yaml

# Batch process all images in a directory
phantom-batch --input input_dir --output output_dir

# Batch process with specific effect and parallel processing
phantom-batch --input input_dir --output output_dir --effect data_glitch --parallel 8
```

## Using with Poetry

```bash
# Install the package
cd packages/phantom-visuals
poetry install

# Run the CLI
poetry run phantom-visuals process input.jpg output.jpg

# Run batch processing
poetry run phantom-batch --input input_dir --output output_dir
```
