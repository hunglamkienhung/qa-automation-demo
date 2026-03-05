import logging

def write_log(logger_names, level, message):
    for name in logger_names:
        level_to_call = {
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR
        }[level]
        logger = logging.getLogger(name)
        if logger.isEnabledFor(level_to_call):
            getattr(logger, level)(message)