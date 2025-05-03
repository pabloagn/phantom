# packages/phantom-visuals/phantom_visuals/transformers/batch_processor.py

"""Batch processor for applying styles to images.

Includes StyleExplorer for comparing multiple styles with the same settings,
and for running predefined 'best flavor' parameter sets for selected styles.
"""

import glob
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import tomllib  # For TOML parsing (Python 3.11+)

# Assuming these are correctly defined and importable:
from phantom_visuals.core.config import (
    ColorScheme,
    Configuration,
    EffectParameters,
    OutputFormat,
    StyleVariant,
)
from phantom_visuals.transformers.author import AuthorTransformer
from phantom_visuals.utils.logging import (
    create_progress_bar,
    get_logger,
    log_error,
    log_processing_step,
    log_success,
    log_warning,
)

logger = get_logger()  # Assuming logger is configured elsewhere (e.g., cli.py or utils)


class StyleExplorer:
    """Explorer for applying styles to images."""

    def __init__(
        self,
        base_config: Optional[Configuration] = None,
        output_dir: Union[
            str, Path
        ] = "output/comparison",  # Default dir for comparisons
    ):
        self.base_config = base_config or Configuration()
        self.output_dir = Path(output_dir)
        # Ensure base config has EffectParameters initialized
        if (
            not hasattr(self.base_config, "effect_params")
            or self.base_config.effect_params is None
        ):
            self.base_config.effect_params = EffectParameters()

    # --- KEEP Existing explore_author_styles ---
    # Allows applying one set of params (from CLI or base_config) to many styles
    def explore_author_styles(
        self,
        input_path: Union[str, Path],
        styles: Optional[List[str]] = None,
        color_schemes: Optional[List[str]] = None,
        intensity: Optional[float] = None,
        blur_radius: Optional[float] = None,
        distortion: Optional[float] = None,
        noise_level: Optional[float] = None,
        grain: Optional[float] = None,
        vignette: Optional[float] = None,
        seed: Optional[int] = None,
        output_format: str = "png",
        # create_comparison: bool = True, # Not used, remove?
    ) -> dict[str, list[Path]]:
        """Apply multiple styles with the SAME parameters to author images."""
        input_paths = self._get_input_paths(input_path)
        if not input_paths:
            raise ValueError(f"No valid images found at {input_path}")

        # Resolve styles and color schemes
        style_variants = self._get_style_variants(styles)
        # Default to base config scheme if none provided
        effective_schemes = (
            color_schemes if color_schemes else [self.base_config.color_scheme.value]
        )
        color_scheme_variants = self._get_color_schemes(effective_schemes)

        # Use dedicated subdirectory for this exploration type relative to the main output_dir
        exploration_output_dir = Path(
            self.output_dir
        )  # Use the directory passed to __init__
        os.makedirs(exploration_output_dir, exist_ok=True)
        results: dict[str, list[Path]] = {}

        base_params = self.base_config.effect_params

        for img_path in input_paths:
            img_name = Path(img_path).stem
            img_output_dir = exploration_output_dir / img_name  # Subdir per image
            os.makedirs(img_output_dir, exist_ok=True)
            log_processing_step(
                logger,
                "Processing Image for Style Comparison",
                f"Image: {img_path.name}",
            )

            for style_name, style_value in style_variants.items():
                for scheme_name, scheme_value in color_scheme_variants.items():
                    # Create parameters, overriding base with provided args if they exist
                    current_params_dict = (
                        base_params.model_dump()
                    )  # Start with base defaults
                    # Override with command-line args if provided
                    if intensity is not None:
                        current_params_dict["intensity"] = intensity
                    if blur_radius is not None:
                        current_params_dict["blur_radius"] = blur_radius
                    if distortion is not None:
                        current_params_dict["distortion"] = distortion
                    if noise_level is not None:
                        current_params_dict["noise_level"] = noise_level
                    if grain is not None:
                        current_params_dict["grain"] = grain
                    if vignette is not None:
                        current_params_dict["vignette"] = vignette
                    if seed is not None:
                        current_params_dict["seed"] = seed

                    try:
                        current_params = EffectParameters(**current_params_dict)
                    except Exception as e:
                        log_error(
                            logger,
                            f"Invalid parameter combination for style {style_name}: {current_params_dict} - Error: {e}",
                        )
                        continue  # Skip this combination

                    config = Configuration(
                        style_variant=StyleVariant(style_value),
                        color_scheme=ColorScheme(scheme_value),
                        output_format=OutputFormat(output_format),
                        effect_params=current_params,
                    )

                    style_key = (
                        f"{style_name.lower()}_{scheme_name.lower()}"
                        if len(color_scheme_variants) > 1
                        else style_name.lower()
                    )
                    output_filename = f"{img_name}_{style_key}.{output_format}"
                    output_file_path = img_output_dir / output_filename

                    log_processing_step(
                        logger,
                        f"Applying Style: {style_name}",
                        f"Color: {scheme_name}, Output: {output_file_path}",
                    )
                    try:
                        # Reuse transformer instance? Maybe not necessary unless huge overhead
                        transformer = AuthorTransformer(config)
                        result_path = transformer.transform(img_path, output_file_path)
                        if style_key not in results:
                            results[style_key] = []
                        results[style_key].append(result_path)
                    except Exception as e:
                        log_error(
                            logger,
                            f"Failed processing {img_path.name} with style {style_key}: {e}",
                        )  # Less verbose errors in batch

            log_success(
                logger,
                f"Completed style comparison for {img_name}",
                {"output_directory": str(img_output_dir)},
            )
        return results

    # --- KEEP explore_abstract_styles (or remove if not used) ---
    def explore_abstract_styles(  # [...] Add parameter overrides similar to explore_author_styles if needed
        self,
        width: int = 1200,
        height: int = 1600,
    ) -> dict[str, list[Path]]:
        log_warning(
            logger,
            "explore_abstract_styles needs review/implementation based on current structure.",
        )
        # Example: Use base config or override specific parameters if provided
        # ... (User's original implementation logic, adapted) ...
        return {}  # Placeholder

    # --- NEW METHOD for running predefined 'flavors' ---
    def run_best_flavors(
        self,
        input_path: Union[str, Path],
        output_dir: Union[str, Path],  # Expects the final desired output dir
        parameter_config_path: Union[str, Path],
        styles_to_run: Optional[List[str]] = None,
        output_format: str = "png",
        default_color_scheme: str = "phantom_core",  # Default color scheme
    ) -> dict[str, Path]:
        """Runs selected styles using predefined parameters from a TOML config file."""
        parameter_config_path = Path(parameter_config_path)
        output_dir = Path(output_dir)

        # Load parameter configurations from TOML
        if not parameter_config_path.is_file():
            log_error(logger, f"Flavor config file not found: {parameter_config_path}")
            raise FileNotFoundError(
                f"Flavor config file not found: {parameter_config_path}"
            )
        try:
            with open(parameter_config_path, "rb") as f:  # Open TOML in binary mode
                style_flavors: Dict[str, Dict[str, Any]] = tomllib.load(f)
            log_success(
                logger, f"Loaded style flavors from {parameter_config_path.name}"
            )
        except tomllib.TOMLDecodeError as e:
            log_error(logger, f"Error decoding TOML from {parameter_config_path}: {e}")
            raise ValueError(f"Invalid TOML in flavor config file: {e}") from e
        except Exception as e:
            log_error(
                logger, f"Error reading flavor config file {parameter_config_path}: {e}"
            )
            raise OSError(f"Could not read flavor config file: {e}") from e

        # Validate input image(s)
        input_paths = self._get_input_paths(input_path)
        if not input_paths:
            log_error(logger, f"No valid images found matching: {input_path}")
            raise ValueError(f"No valid images found matching: {input_path}")

        # Determine which styles to run
        available_styles_in_config = list(style_flavors.keys())
        if styles_to_run:
            run_list_values = [
                s.lower() for s in styles_to_run
            ]  # Use values for matching input
            # Find keys in style_flavors that match the provided values
            run_list_keys = []
            for key, flavor_data in style_flavors.items():
                # Check against both key and potential StyleVariant value if different
                try:
                    style_variant_value = StyleVariant(key).value
                    if style_variant_value in run_list_values:
                        run_list_keys.append(key)
                except ValueError:
                    log_warning(
                        logger,
                        f"Key '{key}' in flavor config is not a valid StyleVariant.",
                    )
                    if key.lower() in run_list_values:  # Also check key directly
                        run_list_keys.append(key)

            # Also check if the input 'styles_to_run' were keys themselves
            for style_input in styles_to_run:
                if (
                    style_input in available_styles_in_config
                    and style_input not in run_list_keys
                ):
                    run_list_keys.append(style_input)

            skipped = [
                s
                for s in styles_to_run
                if s not in run_list_keys and StyleVariant(s).value not in run_list_keys
            ]

            if skipped:
                log_warning(
                    logger,
                    f"Styles skipped (not found in config '{parameter_config_path.name}'): {', '.join(skipped)}",
                )
            if not run_list_keys:
                log_error(
                    logger,
                    "None of the specified styles were found in the flavor configuration file.",
                )
                return {}
            log_processing_step(
                logger,
                f"Attempting to run flavors for styles: {', '.join(run_list_keys)}",
            )
        else:
            # Run all styles defined in the config file
            run_list_keys = available_styles_in_config
            log_processing_step(
                logger,
                f"Running all {len(run_list_keys)} style flavors defined in {parameter_config_path.name}",
            )

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        results: dict[
            str, Path
        ] = {}  # style_name -> output_path (for first image processed)

        # Setup progress bar
        total_tasks = len(input_paths) * len(run_list_keys)
        progress = create_progress_bar(
            f"Running {len(run_list_keys)} Flavors", total=total_tasks, transient=False
        )

        with progress:
            task_id = progress.add_task(
                "[cyan]Processing Flavors...", total=total_tasks
            )

            for img_path in input_paths:
                img_name = Path(img_path).stem

                # Apply each selected style flavor
                for style_key in run_list_keys:
                    flavor_params = style_flavors[style_key]
                    progress.update(
                        task_id,
                        advance=1,
                        description=f"[cyan]Processing: [yellow]{img_name}[/yellow] | Style: [green]{style_key}[/green]",
                    )

                    try:
                        # Validate/create EffectParameters instance from the loaded dict
                        effect_params = EffectParameters(**flavor_params)

                        # Ensure the style key is a valid StyleVariant member value
                        try:
                            style_variant_enum = StyleVariant(style_key)
                        except ValueError:
                            # If the key itself isn't the value, try finding value matching key
                            found = False
                            for member in StyleVariant:
                                if member.name.lower() == style_key.lower():
                                    style_variant_enum = member
                                    found = True
                                    break
                            if not found:
                                log_warning(
                                    logger,
                                    f"Cannot map flavor key '{style_key}' to a valid StyleVariant. Skipping.",
                                )
                                continue

                        # Create specific Configuration for this flavor
                        flavor_config = Configuration(
                            style_variant=style_variant_enum,
                            color_scheme=ColorScheme(
                                default_color_scheme
                            ),  # Use default scheme
                            output_format=OutputFormat(output_format),
                            effect_params=effect_params,
                        )

                        # Define output path directly in the specified output directory
                        output_filename = f"{img_name}_{style_key}.{output_format}"
                        output_file_path = output_dir / output_filename

                        # Create transformer and run transform
                        transformer = AuthorTransformer(flavor_config)
                        result_path = transformer.transform(img_path, output_file_path)

                        # Store result (only for the first image if multiple inputs?) Let's store last path per style
                        results[style_key] = result_path

                        # log_success(logger, f"Successfully applied flavor {style_key}", {"output": str(result_path)}) # Logged by progress

                    except Exception as e:
                        progress.console.print(
                            f"[bold red]Error applying flavor {style_key} to {img_path.name}: {e}[/]"
                        )
                        log_error(
                            logger,
                            f"Failed applying flavor {style_key} to {img_path.name}: {e}"
                        )

        log_success(
            logger,
            "Flavor processing complete.",
            {"outputs_generated": len(results), "output_directory": str(output_dir)},
        )
        return results

    def _get_input_paths(self, input_path: Union[str, Path]) -> list[Path]:
        # (Implementation remains the same as user provided)
        input_path = Path(input_path)
        paths = []
        if isinstance(input_path, str):
            if "*" in input_path or "?" in input_path:
                paths = [Path(p) for p in glob.glob(input_path)]
            else:
                input_path_obj = Path(input_path)
                if input_path_obj.is_file():
                    paths = [input_path_obj]
                elif input_path_obj.is_dir():
                    paths = self._get_images_from_dir(input_path_obj)
        elif isinstance(input_path, Path):
            if input_path.is_file():
                paths = [input_path]
            elif input_path.is_dir():
                paths = self._get_images_from_dir(input_path)

        if not paths:
            log_warning(logger, f"No input images found for path: {input_path}")
        return paths

    def _get_images_from_dir(self, dir_path: Path) -> list[Path]:
        image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif"]
        image_files = []
        for ext in image_extensions:
            image_files.extend(dir_path.glob(f"*{ext}"))
            image_files.extend(dir_path.glob(f"*{ext.upper()}"))
        return image_files

    def _get_style_variants(self, styles: Optional[list[str]] = None) -> dict[str, str]:
        # (Implementation remains the same as user provided)
        all_styles = {style.name: style.value for style in StyleVariant}
        if styles is None or not styles:
            return all_styles
        selected_styles = {}
        styles_lower = [s.lower() for s in styles]
        for name, value in all_styles.items():
            # Match against enum member name OR value (case-insensitive)
            if name.lower() in styles_lower or value.lower() in styles_lower:
                selected_styles[name] = value
        if not selected_styles:
            log_warning(
                logger, f"No specified styles matched available variants: {styles}"
            )
        return selected_styles

    def _get_color_schemes(self, schemes: Optional[list[str]] = None) -> dict[str, str]:
        # (Implementation remains the same as user provided)
        all_schemes = {scheme.name: scheme.value for scheme in ColorScheme}
        if schemes is None or not schemes:
            return {"PHANTOM_CORE": "phantom_core"}  # Default
        if schemes == ["all"]:
            return all_schemes
        selected_schemes = {}
        schemes_lower = [s.lower() for s in schemes]
        for name, value in all_schemes.items():
            if name.lower() in schemes_lower or value.lower() in schemes_lower:
                selected_schemes[name] = value
        if not selected_schemes:
            log_warning(
                logger,
                f"No specified color schemes matched available ones: {schemes}. Using default.",
            )
            return {"PHANTOM_CORE": "phantom_core"}
        return selected_schemes
