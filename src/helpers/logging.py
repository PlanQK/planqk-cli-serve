import logging

from loguru import logger


class LogHandler(logging.Handler):
    def emit(self, record):
        # get Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where the log message originated
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # increase the depth to find the correct caller
        depth += 5  # adjust this value as needed

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
