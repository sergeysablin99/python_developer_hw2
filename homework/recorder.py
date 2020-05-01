import abc


class Recorder(object):
    @abc.abstractmethod
    def __init__(self, classname, source):
        """Инициализировать запись в source"""

    @abc.abstractmethod
    def record(self, obj):
        """Записать/дописать файл"""
