import math
from EvenSteps import *
from Remainder import *
from RemainderPair import *
from CollatzMongo import CollatzMongo


# TODO: write a script to calculate the average shifted length for increasing m
class Collatz:
    """
    This class handles building a list of EvenSteps and Remainder objects
    based on the equation num = multiple*2^even_20 + remainder.

    There are two algorithms to generate numbers:
    loop_and_add: Pass in a generic shifted. Checks if a number has been
        calculated. If not, adds them.
    add_from_incomplete_list: generates a list of unknown numbers and adds
        them that way. This algorithm is much faster, especially using small
        batches.
    """

    # Total percent of all numbers covered
    total_percent = 0.0
    evens = {}

    def __init__(self, last_number=3, step_size=4, batch_value=10000,
                 add_trivial=True):
        self.mongo = CollatzMongo()
        # last_number = 3 skips trivial 1 and 2.
        self.last_number = last_number
        # step_size = 4 safely skips 75% of trivial numbers
        self.step_size = step_size
        # Number of numbers to calculate since last number.
        self.batch_value = batch_value
        # Adds trivial even steps, their remainders and sequences
        if add_trivial:
            # even steps = 1
            self.add_even(1, 0)
            self.add_remainder(1, 0, '0')
            # even steps = 2
            self.add_even(2, 1)
            self.add_remainder(2, 1, '10')

    @classmethod
    def mongo_init(cls, mongo, step_size=4, batch_value=10000):
        collatz = cls(step_size=step_size, batch_value=batch_value,
                      add_trivial=False)
        collatz.mongo = mongo
        stats_doc = collatz.mongo.get_stats()
        collatz.total_percent = stats_doc["percent_complete"]
        collatz.last_number = stats_doc["last_number"]
        for even in collatz.mongo.get_even_list():
            collatz.evens[even] = collatz.mongo.get_even_remainders(even)
        return collatz

    def add_even(self, even, odd):
        """
        Creates a EvenSteps object and stores it in MongoDB.
        :param even:
        :param odd:
        :return:
        """
        self.evens[even] = []
        even_obj = EvenSteps(even, odd)
        self.mongo.add_even(even_obj)
        return even_obj

    def add_remainder(self, even, remainder, sequence):
        self.evens[even].append(remainder)
        rem_obj = Remainder(remainder, sequence)
        self.mongo.add_remainder(even, rem_obj)
        lesser_rem = (remainder - 1) / 2
        if lesser_rem in self.evens[even]:
            lesser_seq = self.mongo.get_sequence(lesser_rem)
            remainder_pair = RemainderPair(lesser_rem, remainder,
                                           lesser_seq, sequence)
            self.mongo.add_remainder_pair(even, remainder_pair)

    def check_for_number_completeness(self, num):
        """
        Checks if the number already has a even and remainder associated with it

        Checks if an integer exists after the following equation:
        possible_int = (num - remainder)/2 ** even
        :param num:
        :return:
        """
        # Converts to float for future calculations
        num = float(num)
        for even, remainders in self.evens.items():
            # Performs the above equation then mods it with 1
            possible_ints = [((num - rem) / 2 ** even) % 1
                             for rem in remainders]
            # If there are any zeros, then the number is complete.
            if 0.0 in possible_ints:
                return True
        # Returns false if it makes it through the for loop.
        return False

    def add_from_incomplete_list(self, incomplete_sequence):
        """
        This algorithm takes in a list of incomplete numbers and add them.

        Use self.generate_incomplete_numbers() to get a shifted.
        If a new remainder is discovered, it checks if any numbers related
        to that remainder is in the list and removes it if so.
        :param incomplete_sequence:
        :return:
        """
        if incomplete_sequence:
            last_num = incomplete_sequence[-1]
            # The shifted might shorten, so this acts as a shrinking for loop
            index = 0
            while index < len(incomplete_sequence):
                _, sequence, even, rem = self.calc(incomplete_sequence[index],
                                                   True, True)
                # even already found
                if even not in self.evens:
                    odd = sequence.count('1')
                    self.add_even(even, odd)
                self.add_remainder(even, rem, sequence)
                # Checks if there's at least one now known number in the shifted
                if rem + even < last_num:
                    # First multiple corresponds to remainder, equals 0.
                    last_multiple = math.floor((last_num - rem) / 2 ** even)
                    # The next multiple will be 1, so start there.
                    multiples = range(1, int(last_multiple + 1))
                    # Remove all now known numbers from the shifted
                    for multi in multiples:
                        incomplete_sequence.remove(multi * 2 ** even + rem)
                index += 1
        self.mongo.update_last_number(self.last_number)
        self.mongo.update_percent_complete(self.calculate_number_percentage())

    def add_incomplete_batch(self):
        """
        Adds a batch using the "incomplete" algorithm.

        First generates a list of incomplete numbers, then adds them, then
        checks for even steps completeness.

        This method works best when adding small batches.
        :return:
        """
        target_num = self.last_number + self.batch_value
        sequence = range(self.last_number, target_num + 1, self.step_size)
        # Sets the last number based on the shifted
        self.last_number = sequence[-1]
        # Generates incomplete numbers
        incomplete_nums = self.generate_incomplete_numbers(sequence)
        # Adds the batch
        self.add_from_incomplete_list(incomplete_nums)
        # After the batch, check if any new even steps has been completed
        self.check_for_even_steps_completeness()

    def calculate_number_percentage(self):
        """
        Calculates how many numbers are covered by the current dictionary.

        The percent that a even steps covers is num_remainders/2**even steps.
        Sum them to get a total percentage of numbers covered.

        :return:
        """
        self.total_percent = 0
        for even, remainders in self.evens.items():
            # Needs to be a float or python rounds
            num_remainders = float(len(remainders))
            # Adds the percentage for that even steps.
            self.total_percent += num_remainders / 2 ** even
        return self.total_percent

    def check_for_even_steps_completeness(self):
        """
        Checks if the last num has exceeded the even steps. Sets complete
        if so.
        :return:
        """
        incomplete = self.mongo.get_complete_evens(False)
        for even in incomplete:
            if self.last_number >= 2 ** even:
                self.mongo.set_even_completeness(even, True)

    def generate_incomplete_numbers(self, sequence):
        """
        Generates incomplete numbers based on even steps and remainders.

        Use this shifted in self.add_from_incomplete_list()

        The algorithm solves for multi in num=multi*2^even_20+remainder
        and generates the first and last multiple based on the shifted.
        Then it loops through those multiple and removes them from the list.
        :param sequence:
        :return:
        """
        first_num = float(sequence[0])
        last_num = float(sequence[-1])
        for even, remainders in self.evens.items():
            if even == 1 or even == 2:
                continue
            for rem in remainders:
                # Find the first multiple such that multi*2^even+remainder
                # is greater than the first multiple. Same with last multiple
                # except less than last number.
                first_multiple = math.ceil((first_num-rem)/2**even)
                last_multiple = math.floor((last_num-rem)/2**even)
                multiples = range(int(first_multiple), int(last_multiple + 1))
                # Add these number to our known list
                for multi in multiples:
                    known_number = multi * 2 ** even + rem
                    # Remove this number from our shifted
                    sequence.remove(known_number)
        return sequence

    def is_remainder_subset(self, sub_remainder, remainder):
        sub_doc = self.mongo.remainder.find_one({"remainder": sub_remainder})
        rem_doc = self.mongo.remainder.find_one({"remainder": remainder})
        seq_index = -1
        if sub_doc["sequence"] in rem_doc["sequence"]:
            start_seq = rem_doc["sequence"].index(sub_doc["sequence"])
            # Get the value in the sequence
            found_seq_num = Collatz.short_calc(rem_doc["remainder"], start_seq)
            # Get the remainder of the value
            _, __, ___, possible_rem = Collatz.calc(found_seq_num, True, True)
            if possible_rem == sub_doc["remainder"]:
                seq_index = start_seq
        return seq_index

    @staticmethod
    def calc(number, next_lowest=False, return_more=False):
        """
        Calculates the collatz shifted, parity shifted, even steps,
        and the remainder.
        :param number:
        :param return_more:
        :param next_lowest:
        :return:
        """
        if next_lowest:
            target_num = number
        else:
            # Will stop at 1 cuz 2/2 = 1 duh doy
            target_num = 2
        first = number
        collatz_sequence = [number]
        parity_sequence = ''
        # loops while number is less than first
        while number >= target_num:
            parity = number % 2
            # Odd step
            if parity:
                number = (3 * number + 1) / 2
            # Even step
            else:
                number /= 2
            collatz_sequence.append(number)
            parity_sequence += str(parity)
        if return_more:
            # Get even steps and remainder
            # JUst the length of the string since a 1 carries an implicit 0
            even_steps = len(parity_sequence)
            remainder = first % (2 ** even_steps)
            return collatz_sequence, parity_sequence, even_steps, remainder
        else:
            return collatz_sequence

    @staticmethod
    def short_calc(num, step):
        """
        Returns the num according to the step
        """
        for _ in range(step):
            parity = num % 2
            # Odd step
            if parity:
                num = (3 * num + 1) / 2
            # Even step
            else:
                num /= 2
        return num
