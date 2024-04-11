import logging

from loguru import logger

log = logging.getLogger(__name__)


def run(**kwargs):
    data = kwargs.get('data', {})
    params = kwargs.get('params', {})

    print("print - data: ", data)
    print("print - params: ", params)

    log.info("logging - data: %s", data)
    log.info("logging - params: %s", params)

    logger.info("loguru - data: {}", data)
    logger.info("loguru - params: {}", params)

    return {data: data, params: params}
