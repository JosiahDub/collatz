from typing import Dict

import pandas as pd

from CollatzContainer import CollatzContainer

from EvenSteps import EvenSteps
from Remainder import Remainder
from RemainderPair import RemainderPair


class CollatzPandas(CollatzContainer):

    def even_exists(self, even: int):
        pass

    def even_complete(self, even: int):
        pass

    def set_even_completeness(self, even: int, complete: bool):
        pass

    def get_even_list(self):
        pass

    def get_complete_evens(self, complete: bool):
        pass

    def add_remainder(self, even: EvenSteps, rem: Remainder):
        pass

    def add_remainder_pair(self, even: int, pair: RemainderPair):
        pass

    def remainder_exists(self, even: int, rem: int):
        pass

    def get_num_remainders(self, even: int):
        pass

    def get_remainder_pair_sequence(self, pair: list):
        pass

    def get_even_remainders(self, even: int):
        pass

    def get_sequence(self, remainder: int):
        pass

    def update_last_number(self, number: int):
        pass

    def get_last_number(self):
        pass

    def update_percent_complete(self, percent: float):
        pass

    def get_stats(self):
        pass

    def __init__(self):
        super().__init__()

    def add_even(self, even: EvenSteps):
        pass


