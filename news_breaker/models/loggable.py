from news_breaker.utils.logger import get_logger


class Loggable(type):
    def __init__(self, clsname, bases, attrs):
        super().__init__(clsname, bases, attrs)
        # Explicit name mangling
        logger_attribute_name = "_" + self.__name__ + "__logger"

        # Logger name derived accounting for inheritance for the bonus marks
        logger_name = ".".join([c.__name__ for c in self.mro()[-2::-1]])

        setattr(self, logger_attribute_name, get_logger(logger_name))
