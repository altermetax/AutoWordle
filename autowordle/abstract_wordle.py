from abc import ABC, abstractmethod

class AbstractWordle:
    def __init__(self, data_path):
        pass

    @abstractmethod
    def try_word(self, guess):
        pass