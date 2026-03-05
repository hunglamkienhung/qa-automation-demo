import logging
import os
import re
from datetime import datetime
from contextlib import contextmanager

@contextmanager
def log_context(base_log_dir, filename='', log_types=('Pass', 'Fail', 'Error', 'All')):
    loggers, handlers = {}, []
    filename = re.sub(r'[^\w\-]', '_', filename.strip()) or datetime.now().strftime("%Y%m%d_%H%M%S")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    level_map = {'Pass': logging.INFO, 'Fail': logging.WARNING, 'Error': logging.ERROR, 'All': logging.INFO}

    try:
        for log_type in log_types:
            log_dir = os.path.join(base_log_dir, log_type)
            os.makedirs(log_dir, exist_ok=True)
            path = os.path.join(log_dir, f"{filename}.log")

            logger = logging.getLogger(log_type.lower())
            logger.setLevel(logging.DEBUG)  # Để ghi đủ các mức nếu cần
            fh = logging.FileHandler(path, mode='a', encoding='utf-8-sig')
            fh.setLevel(level_map.get(log_type, logging.INFO))
            fh.setFormatter(formatter)

            logger.addHandler(fh)
            logger.propagate = False
            loggers[log_type.lower()] = logger
            handlers.append((logger, fh))
        yield loggers

    finally:
        for logger, handler in handlers:
            logger.info("✅ Close logger và file_handler.")
            handler.close()
            logger.removeHandler(handler)
            if os.path.exists(handler.baseFilename) and os.path.getsize(handler.baseFilename) == 0:
                os.remove(handler.baseFilename)
