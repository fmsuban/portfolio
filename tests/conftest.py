import os
import sys


# Make sure the `src/` directory is available during test collection.
# This enables imports like `from portfolio.stock import Stock`.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_DIR)

