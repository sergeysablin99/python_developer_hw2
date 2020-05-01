import abc


class Reader(object):
    @abc.abstractmethod
    def __init__(self, classname, source):
        """Инициализировать чтение из source"""

