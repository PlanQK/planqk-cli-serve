import logging

from loguru import logger


def run(**kwargs):
    data = kwargs.get('data', {})
    params = kwargs.get('params', {})

    print("print - data: ", data)
    print("print - params: ", params)

    logging.info("logging - data: {}", data)
    logging.info("logging - params: {}", params)

    logger.info("loguru - data: {}", data)
    logger.info("loguru - params: {}", params)

    return {data: data, params: params}
