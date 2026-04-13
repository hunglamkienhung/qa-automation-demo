import logging

from config.settings import settings

def _configure_root_logger() -> None:

    # Map string log level to logging constant (INFO, DEBUG, etc.)
    level = getattr(logging, settings.log_level, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


# Configure the logger at import time
_configure_root_logger()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
