from typing import Dict

import pandas as pd

from CollatzContainer import CollatzContainer

from EvenSteps import EvenSteps
from Remainder import Remainder
from RemainderPair import RemainderPair


class CollatzPandas(CollatzContainer):

    """
    DataFrame Structure
    EVEN
    Even, Odd, Completed, Alpha

    REMAINDER
    remainder, even, sequence, beta, num_initial_increases, num_trailing_decreases, sequence_center

    REMAINDER PAIR
    pair, even, shifted_core
    """

    def __init__(self):
        super().__init__()
        self.even = pd.DataFrame(columns=['odd',
                                          'completed',
                                          'alpha',
                                          ],
                                 index=pd.Index([], name='even'))
        self.remainder = pd.DataFrame(columns=['even',
                                               'sequence',
                                               'beta',
                                               'num_initial_increases',
                                               'num_trailing_decreases',
                                               'sequence_center',
                                               ],
                                      index=pd.Index([], name='remainder'))
        self.pair = pd.DataFrame(columns=['even',
                                          'shifted_core',
                                          ],
                                 index=pd.Index([], name='pair'))

    """
    EVENS
    """

    def add_even(self, even: EvenSteps):
        self.even.loc[even.even_steps] = [even.odd_steps, even.completed, even.alpha]

    def even_exists(self, even: int):
        return even in self.even.index

    def even_complete(self, even: int):
        return self.even.at[even, 'completed']

    def set_even_completeness(self, even: int, complete: bool):
        self.even.at[even, 'completed'] = complete

    def get_even_list(self):
        return list(self.even.index.values)

    def get_complete_evens(self, complete: bool):
        pass

    """
    REMAINDER
    """

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

    """
    STATS
    """

    def update_last_number(self, number: int):
        pass

    def get_last_number(self):
        pass

    def update_percent_complete(self, percent: float):
        pass

    def get_stats(self):
        pass
