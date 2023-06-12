try:
    from loguru import logger
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
