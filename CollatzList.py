from typing import Dict

from CollatzContainer import *

# TODO: Save and load files


class CollatzList(CollatzContainer):
    """
    Simple container to hold everything in dictionaries and lists.
    """

    last_number: int
    percent_complete: float

    def __init__(self):
        super().__init__()
        self.evens: Dict[int, dict] = {}
        self.remainders: Dict[int, Remainder] = {}

    def add_even(self, even: EvenSteps):
        self.evens[even.even_steps] = {'even': even, 'remainders': {}}

    def even_exists(self, even: int):
        return even in self.evens

    def even_complete(self, even: int):
        return self.evens[even]['even'].completed

    def set_even_completeness(self, even: int, complete: bool):
        self.evens[even]['even'].completed = complete

    def get_even_list(self):
        return self.evens.keys()

    def get_complete_evens(self, complete: bool):
        return [even for even, even_info in self.evens.items() if even_info['even'].completed]

    """
    REMAINDER
    """

    def add_remainder(self, even: EvenSteps, rem: Remainder):
        self.evens[even.even_steps]['remainders'][rem.remainder] = Remainder

    def add_remainder_pair(self, even: int, pair: RemainderPair):
        raise NotImplementedError

    def remainder_exists(self, even: int, rem: int):
        return rem in self.evens[even]['remainders']

    def get_num_remainders(self, even: int):
        return len(self.evens[even]['remainders'])

    def get_remainder_pair_sequence(self, pair: list):
        raise NotImplementedError

    def get_even_remainders(self, even: int):
        return self.evens[even]['remainders'].keys()

    def get_sequence(self, remainder: int):
        raise NotImplementedError

    """
    # STATS
    """

    def update_last_number(self, number: int):
        self.last_number = number

    def get_last_number(self):
        return self.last_number

    def update_percent_complete(self, percent: float):
        self.percent_complete = percent

    def get_stats(self):
        return {'percent_complete': self.percent_complete, 'last_number': self.last_number}

    """
    SAVE AND LOAD
    """
    def save(self, path: str):
        pass

    def load(self, files: dict):
        pass

    """
    UTILITIES
    """
    def check_for_number_completeness(self, num):
        """
        Checks if the number already has a even and remainder associated with it

        Checks if an integer exists after the following equation:
        possible_int = (num - remainder)/2 ** even
        :param num:
        :return:
        """
        for even, remainders in self.evens.items():
            # Performs the above equation then mods it with 1
            possible_ints = [((num - rem) / 2 ** even) % 1
                             for rem in remainders]
            # If there are any zeros, then the number is complete.
            if 0.0 in possible_ints:
                return True
        # Returns false if it makes it through the for loop.
        return False
