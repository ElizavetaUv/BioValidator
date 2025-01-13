import logging
import sys

logger = logging.getLogger("bio-validator")
logger.addHandler(logging.NullHandler())


def init_logger(level: str) -> None:
    # TODO: Add sterr handler or convert it into dict config
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    logger.setLevel(level)
