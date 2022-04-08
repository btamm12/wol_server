from datetime import datetime
import logging
import os
import traceback


logger = logging.getLogger(__name__)


def default_logger_path(src_dir="."):
    """
    Returns the default logger path, relative to `app.py`.

    File path:
    ```
    ../logs/app/[date].log
    ```
    """
    dt_str = datetime.now().replace(microsecond=0).isoformat()
    dt_str = dt_str.replace(":", "-")
    path = os.path.join(src_dir, os.pardir, "logs", "app", dt_str + ".log")
    path = os.path.realpath(path)
    return path


def log_exception(logger: logging.Logger, e: Exception):
    logger.warning(e)
    logger.warning(traceback.format_exc())


def logger_setup(
    fmt: str,
    console_level: int,
    file_level: int = None,
    file_path: str = None,
):
    """Set up the logger globally."""
    if file_level is None:
        file_level = console_level

    min_level = min(console_level, file_level)
    logger.setLevel(min_level)

    # Create formatter for logger(s).
    formatter = logging.Formatter(fmt)

    # Create console logger.
    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Create file logger.
    if file_path is not None:

        # Make sure directory exists.
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        fh = logging.FileHandler(file_path)
        fh.setLevel(file_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
