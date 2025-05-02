# Phantom Visuals

<div align="center">

_A sophisticated Python toolkit for image manipulation and transformation with distinctive Phantom aesthetics._

</div>

<br/>
<div align="center">───────  §  ───────</div>
<br/>

## Vision & Approach

In the digital realm where visual identity is paramount, Phantom Visuals provides a flexible, programmable approach to image transformation. Built for the Phantom aesthetic universe, it addresses the need for a distinctive visual signature across images while enabling creative exploration.

Our core goals are:

- **Visual Identity:** Create a recognizable visual language for the Phantom ecosystem
- **Artistic Freedom:** Offer flexible tools for creative image manipulation
- **Reproducibility:** Enable consistent, seed-based transformations
- **Modular Architecture:** Allow for easy extension and customization

Phantom Visuals bridges the gap between computational art and practical application, enabling the creation of cohesive visual assets with a distinctive modern, eerie, and minimalist aesthetic.

<br/>
<div align="center">───────  §  ───────</div>
<br/>

## Features

- **Author Transformations:** Apply distinctive styles to author portraits
- **Abstract Compositions:** Generate abstract art with various aesthetic approaches
- **Digital Glitch Effects:** Create digital art with glitch aesthetics and data manipulation
- **Color Harmonization:** Leverage phantom-core design system colors
- **Powerful CLI:** Command-line interface for easy experimentation and batch processing
- **Reproducible Outputs:** Seed-based generation for consistent results
- **Configuration Profiles:** Save and load parameter combinations
- **Comprehensive Logging:** Detailed logs for debugging and tracking transformations

## Installation

Phantom Visuals is managed with Poetry for dependency management:

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the package directory
cd packages/phantom-visuals

# Install with Poetry
poetry install

# Alternatively, install in development mode
poetry install --dev
```

## Quick Start

### Command Line Usage

Phantom Visuals provides a powerful CLI for quick experimentation:

```bash
# Transform an image with the default phantom style
phantom-visuals transform input.jpg -o output.png

# Apply a specific style with custom parameters
phantom-visuals transform input.jpg -o output.png --style gothic --intensity 0.8 --grain 0.4

# Process multiple images with the same settings
phantom-visuals transform "input/*.jpg" -o output_dir --batch

# Generate an abstract composition
phantom-visuals create -o abstract.png --style abstract --width 1200 --height 1600

# Create multiple variations with different seeds
phantom-visuals create -o compositions/comp.png --count 5

# List available styles
phantom-visuals styles

# Save a configuration profile
phantom-visuals config --name gothic_portrait --style gothic --intensity 0.8 --grain 0.4

# Enable debug logging for detailed information
phantom-visuals transform input.jpg -o output.png --log-level DEBUG
```

### Python API Usage

For more control, you can use the Python API directly:

```python
from phantom_visuals.core import Configuration, StyleEngine
from phantom_visuals.transformers import AuthorTransformer, AbstractComposer
from phantom_visuals.effects import EffectChain, add_grain, gaussian_blur

# Simple image transformation with default settings
transformer = AuthorTransformer()
transformer.transform("input.jpg", "output.png")

# More customized transformation
config = Configuration(
    style_variant="phantom",
    color_scheme="phantom_core",
    effect_params={"intensity": 0.8, "grain": 0.4, "blur_radius": 5.0}
)

transformer = AuthorTransformer(config)
transformer.transform("input.jpg", "output.png")

# Create an abstract composition
composer = AbstractComposer(config)
composer.create_composition(width=1200, height=1600, output_path="abstract.png")

# Using the Style Engine directly with custom effects
engine = StyleEngine(config)
engine.add_transformation(add_grain)
engine.add_transformation(lambda img, cfg, pal: gaussian_blur(img, cfg, pal, 3.0))
engine.transform("input.jpg", "output.png")
```

## Available Styles

Phantom Visuals includes a variety of predefined styles:

### Author Transformation Styles

- **minimal:** Clean, pixelated representation with minimal artistic intervention
- **duotone:** Two-tone color mapping using phantom-core color palette
- **abstract:** Artistic interpretation with geometric elements
- **ethereal:** Dreamy, soft aesthetic with blurs and ethereal glow
- **modernist:** Bold geometric minimalism inspired by modernist design
- **phantom:** Signature Phantom style with distinctive transformations
- **gothic:** Dark, moody aesthetic with dramatic contrast
- **symmetrical:** Symmetrical compositions with kaleidoscopic effects

### Digital Art Styles

- **glitch:** Digital glitch aesthetic with channel shifts and sorting
- **pixel:** Pixel art aesthetic with pronounced pixelation
- **databend:** Data corruption aesthetic with digital artifacts
- **scan:** Scanner/copy machine aesthetic with halftones and scan lines
- **vaporwave:** Nostalgic vaporwave aesthetic with distinctive colors
- **cyberpunk:** Neon cyberpunk aesthetic with edge detection
- **digital_decay:** Digital decay aesthetic with corruption artifacts
- **compression:** Compression artifacts aesthetic inspired by lossy compression

## Customization Parameters

Fine-tune transformations with these parameters:

- **intensity:** Overall effect strength (0.0-1.0)
- **blur_radius:** Amount of blur to apply (0.0-50.0)
- **distortion:** Spatial distortion amount (0.0-1.0)
- **noise_level:** Random noise intensity (0.0-1.0)
- **grain:** Film grain amount (0.0-1.0)
- **vignette:** Vignette effect strength (0.0-1.0)
- **seed:** Random seed for reproducible results
- **log-level:** Set logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Logging

Phantom Visuals includes a comprehensive logging system that records all operations, parameters, and potential errors. This is useful for debugging and tracking the history of transformations.

### Log Features

- **Automatic Log Directory:** Creates a `logs` directory to store log files
- **Daily Log Files:** Organizes logs by date (e.g., `phantom_visuals_20230801.log`)
- **Rich Formatting:** Console logs are formatted with color and style using Rich
- **Configurable Verbosity:** Adjust log detail with the `--log-level` parameter
- **Detailed Error Tracking:** Full tracebacks with context information
- **Configuration Recording:** Logs all parameters for reproducibility

### Log Levels

- **DEBUG:** Detailed information for troubleshooting
- **INFO:** General execution and operation information (default)
- **WARNING:** Issues that might cause problems
- **ERROR:** Errors that prevented an operation from completing
- **CRITICAL:** Critical errors requiring immediate attention

### Setting Log Level

You can set the logging level using the `--log-level` parameter in any CLI command:

```bash
phantom-visuals transform input.jpg -o output.png --log-level DEBUG
```

Or in Python code:

```python
from phantom_visuals.utils.logging import setup_logging
logger = setup_logging(level="DEBUG")
```

## Architecture

Phantom Visuals follows a modular architecture for maximum flexibility:

```
phantom_visuals/
├── core/                # Core functionality
│   ├── config.py        # Configuration management
│   ├── engine.py        # Style engine
│   └── palette.py       # Color palette handling
├── effects/             # Image processing effects
│   ├── base.py          # Base effect chain
│   ├── blur.py          # Blur effects
│   ├── color.py         # Color transformations
│   ├── distortion.py    # Distortion effects
│   ├── edge.py          # Edge detection effects
│   ├── texture.py       # Texture and grain effects
│   └── artistic.py      # Artistic transformations
├── transformers/        # High-level transformers
│   ├── author.py        # Author portrait transformers
│   ├── abstract.py      # Abstract art generators
│   └── digital.py       # Digital art transformers
├── utils/               # Utility modules
│   └── logging.py       # Logging configuration
├── cli.py               # Command-line interface
└── __init__.py          # Package exports
```

## Configuration Management

Save and load configurations for consistent results:

```bash
# Create and save a configuration
phantom-visuals config --name dark_portrait --style gothic --intensity 0.9 --grain 0.5

# Use the saved configuration
phantom-visuals transform input.jpg -o output.png --load-config configs/dark_portrait.json
```

## Examples

Examples of various styles and effects are available in the `examples` directory.

## Contributing

We welcome contributions to Phantom Visuals! Please feel free to submit issues or pull requests.

## License

[MIT](./LICENSE)

---

<div align="center">
<img src="references/original.jpg" width="200" alt="Phantom Visuals Example">
</div>
<div align="center">
<i>Phantom Visuals: Transforming the ordinary into the extraordinary</i>
</div>
