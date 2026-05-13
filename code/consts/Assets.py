import sys
from pathlib import Path

def get_assets_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent.parent.parent

    assets_path = base_path / "assets"
    return assets_path


def get_asset_file(filename):
    return get_assets_path() / filename

ASSETS_DIR = get_assets_path()
