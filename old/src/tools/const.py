from pathlib import Path

__all__ = (
    "PROJECT_ROOT",
    "OUTPUT_DIR",
)


PROJECT_ROOT = Path(__file__).joinpath("../../../").resolve()
OUTPUT_DIR = PROJECT_ROOT.joinpath("out").resolve()

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
