import os
from typing import List
from pathlib import Path


def get_dirs(path: Path) -> List[Path]:
    return [path / f for f in os.listdir(path) if (path / f).is_dir()]


def get_files(path: Path) -> List[Path]:
    return [path / f for f in os.listdir(path) if (path / f).is_file()]
