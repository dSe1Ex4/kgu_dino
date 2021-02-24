from abc import ABCMeta, abstractmethod, abstractproperty


class IStorage:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def save(score: int):
        """Метод сохранения"""

    @staticmethod
    @abstractmethod
    def get():
        """Метод выгрузки"""


class FileSave(IStorage):
    @staticmethod
    def save(score: int):
        with open("score.txt", "w") as file:
            file.write(str(score))

    @staticmethod
    def get():
        with open("score.txt", "r") as file:
            return int(file.readline())
