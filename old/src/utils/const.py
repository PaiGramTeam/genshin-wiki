from pathlib import Path

PROJECT_ROOT = Path(__file__).joinpath("../../").resolve()
DATA_DIR = PROJECT_ROOT.joinpath("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE_PATH = DATA_DIR.joinpath("db.sqlite")

NOT_SET = object()
