from abc import ABC, abstractmethod

class AbstractWordle:
    @abstractmethod
    def try_word(self, word):
        pass