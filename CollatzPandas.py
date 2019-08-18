import pandas as pd

from CollatzContainer import *


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
        self.even = pd.DataFrame({'odd': pd.Series([], dtype='int64'),
                                  'completed': pd.Series([], dtype='bool'),
                                  'alpha': pd.Series([], dtype='float64')
                                  },
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
                                 index=pd.MultiIndex(levels=[[], []],
                                                     codes=[[], []],
                                                     names=['first', 'second']))
        self.stats = pd.Series({'Last Number': 0, 'Percent Complete': 0})

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
        return [int(e) for e in self.even.index.values]

    def get_complete_evens(self, complete: bool):
        return list(self.even.loc[self.even['completed'] == complete].index)

    """
    REMAINDER
    """

    def add_remainder(self, even: int, rem: Remainder):
        self.remainder.loc[rem.remainder] = [even,
                                             rem.sequence,
                                             rem.beta,
                                             rem.num_initial_increases,
                                             rem.num_trailing_decreases,
                                             rem.sequence_center,
                                             ]

    def remainder_exists(self, even: int, rem: int):
        return rem in self.remainder.index

    def get_num_remainders(self, even: int):
        return self.remainder

    def get_even_remainders(self, even: int):
        return list(self.remainder.loc[self.remainder['even'] == even].index)

    def get_sequence(self, remainder: int):
        return self.remainder.at[remainder, 'sequence']

    """
    REMAINDER PAIR
    """

    def add_remainder_pair(self, even: int, pair: RemainderPair):
        self.pair.loc[tuple(pair.pair), 'even'] = even
        self.pair.loc[tuple(pair.pair), 'shifted_core'] = pair.shifted_core

    def get_remainder_pair_sequence(self, pair: list):
        return [self.remainder.at[pair[0], 'sequence'], self.remainder.at[pair[1], 'sequence']]

    """
    STATS
    """

    def update_last_number(self, number: int):
        self.stats['Last Number'] = number

    def get_last_number(self):
        return self.stats['Last Number']

    def update_percent_complete(self, percent: float):
        self.stats['Percent Complete'] = percent

    def get_stats(self):
        return {'percent_complete': self.stats['Percent Complete'], 'last_number': self.stats['Last Number']}

    """
    SAVE AND LOAD
    """

    def save(self, path: str = ''):
        self.even.to_pickle(os.path.join(path, 'even.pkl'))
        self.remainder.to_pickle(os.path.join(path, 'remainder.pkl'))
        self.pair.to_pickle(os.path.join(path, 'pair.pkl'))
        self.stats.to_pickle(os.path.join(path, 'stats.pkl'))

    @classmethod
    def load(cls, files: dict):
        self = cls()
        self.even = pd.read_pickle(files['even'])
        self.remainder = pd.read_pickle(files['remainder'])
        self.pair = pd.read_pickle(files['pair'])
        self.stats = pd.read_pickle(files['stats'])
        return self

    """
    UTILITIES
    """

    def check_for_number_completeness(self, num: int):
        pos = (num - self.remainder.index).values / 2 ** self.remainder['even'] % 1
        return 0 in pos
