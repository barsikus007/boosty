from typing import TYPE_CHECKING

try:
    from loguru import logger  # type: ignore
except ImportError:
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        # format=(
        #     "%(filename)s:\t"
        #     "%(levelname)s:\t"
        #     "%(funcName)s():\t"
        #     "%(lineno)d:\t"
        #     "%(message)s")
    )
    logger = logging.LoggerAdapter(logging.getLogger(__name__.split(".")[0]))

if TYPE_CHECKING:
    import logging

    logger = logging.LoggerAdapter(logging.getLogger(__name__.split(".")[0]))
