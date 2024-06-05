import logging.config

from constants import Constants as C


def configure_main_logger(logger_name):
    logging.config.fileConfig(
        C.LOGGING_PATH / C.LOGGING_CONFIG_FILENAME, disable_existing_loggers=False
    )
    logger = logging.getLogger(logger_name)
    return logger
