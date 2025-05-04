#!/usr/bin/env python

"""Wrapper script to directly run phantom-visuals commands.

This allows testing the CLI without installation.
"""

import os
import sys

# Add the src directory to the path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

from phantom_visuals_v2.cli import batch, cli

if __name__ == "__main__":
    # If no arguments or first argument is "batch", run batch command
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        # Remove the "batch" argument
        sys.argv.pop(1)
        batch()
    else:
        cli()
