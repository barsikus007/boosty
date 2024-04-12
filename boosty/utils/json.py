from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    json: ModuleType

try:
    from orjson import json  # type: ignore
    module = "orjson"
except ImportError:
    import json
    module = "json"


def dict_to_file(data: dict, filename: Path | str):
    to_dump = json.dumps(data)
    with open(filename, "wb" if module == "orjson" else "w") as f:
        f.write(to_dump)


def file_to_dict(filename: Path | str) -> dict:
    with open(filename, "rb" if module == "orjson" else "r") as f:
        return json.loads(f.read())
