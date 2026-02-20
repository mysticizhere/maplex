from pathlib import Path

import ujson
from mcp.client.stdio import logger


def json_file_to_dict(file: str) -> dict:
    try:
        with open(file=file) as config_file:
            config = ujson.load(config_file)
            return config
    except (TypeError, FileNotFoundError, ValueError) as exception:
        logger.error("Failed to parse json file : %s", file, exc_info=True)
        raise exception


def _load_config() -> dict:
    """Load config.json from project root (parent of app package)."""
    try:
        # Resolve path from this file: app/utils/common_utils.py -> project root
        root = Path(__file__).resolve().parent.parent.parent
        return json_file_to_dict(str(root / "config.json"))
    except (TypeError, FileNotFoundError, ValueError):
        return {}


class CONFIG:
    config: dict = _load_config()

