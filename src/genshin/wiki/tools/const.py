import os
from pathlib import Path

__all__ = (
    "PKG_DIR",
    "DATA_DIR",
    "PROJECT_ROOT",
    "CACHE_DIR",
)


PKG_DIR = Path(__file__).joinpath("../../").resolve()
"""The root directory of the package."""

DATA_DIR = PKG_DIR.joinpath("data")
"""The directory where data files are stored."""
DATA_DIR.mkdir(parents=True, exist_ok=True)

PROJECT_ROOT = Path(os.curdir).resolve()
"""The root directory of the project."""


CACHE_DIR = PKG_DIR.joinpath("cache")
"""The directory where cache files are stored."""
CACHE_DIR.mkdir(parents=True, exist_ok=True)
