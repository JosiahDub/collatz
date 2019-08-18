import os

from EvenSteps import EvenSteps
from Remainder import Remainder
from RemainderPair import RemainderPair


class CollatzContainer:
    """
    A base class to hold Collatz info. Can connect to MongoDB, or simply hold some lists.
    """
    def __init__(self):
        pass

    def add_even(self, even: EvenSteps):
        raise NotImplementedError

    def even_exists(self, even: int):
        raise NotImplementedError

    def even_complete(self, even: int):
        raise NotImplementedError

    def set_even_completeness(self, even: int, complete: bool):
        raise NotImplementedError

    def get_even_list(self):
        raise NotImplementedError

    def get_complete_evens(self, complete: bool):
        raise NotImplementedError

    """
    REMAINDER
    """

    def add_remainder(self, even: int, rem: Remainder):
        raise NotImplementedError

    def add_remainder_pair(self, even: int, pair: RemainderPair):
        raise NotImplementedError

    def remainder_exists(self, even: int, rem: int):
        raise NotImplementedError

    def get_num_remainders(self, even: int):
        raise NotImplementedError

    def get_remainder_pair_sequence(self, pair: list):
        raise NotImplementedError

    def get_even_remainders(self, even: int):
        raise NotImplementedError

    def get_sequence(self, remainder: int):
        raise NotImplementedError

    """
    STATS
    """

    def update_last_number(self, number: int):
        raise NotImplementedError

    def get_last_number(self):
        raise NotImplementedError

    def update_percent_complete(self, percent: float):
        raise NotImplementedError

    def get_stats(self):
        raise NotImplementedError

    """
    SAVE AND LOAD
    """

    def save(self, path: str):
        raise NotImplementedError

    def load(self, files: dict):
        raise NotImplementedError

    """
    UTILITIES
    """

    def check_for_number_completeness(self, num: int):
        raise NotImplementedError

