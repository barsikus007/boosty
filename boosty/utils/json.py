from typing import TYPE_CHECKING

from boosty.utils.types import StrPath

if TYPE_CHECKING:
    from types import ModuleType

    json: ModuleType

try:
    from orjson import json  # pyright: ignore[reportAttributeAccessIssue]

    module = "orjson"
except ImportError:
    import json

    module = "json"


def dict_to_file(data: dict, filename: StrPath):
    to_dump = json.dumps(data)
    with open(filename, "wb" if module == "orjson" else "w") as f:
        f.write(to_dump)


def file_to_dict(filename: StrPath) -> dict:
    with open(filename, "rb" if module == "orjson" else "r") as f:
        return json.loads(f.read())
