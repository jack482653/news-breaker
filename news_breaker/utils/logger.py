import logging
import logging.config

import yaml

from news_breaker.config import get_project_path

is_configured = False


def get_logger(name=None):
    global is_configured

    if not is_configured:
        with open(get_project_path("logging.yml"), "r") as stream:
            config = yaml.load(stream, Loader=yaml.FullLoader)
            logging.config.dictConfig(config)
            is_configured = True

    return logging.getLogger(name)
