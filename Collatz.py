__author__ = 'josiah'
from EvenSteps import *
import math


# TODO: write a script to calculate the average shifted length for increasing m
class Collatz:
    """ This class handles building a list of EvenSteps and Remainder objects
        based on the equation num = multiple*2^even_20 + remainder.

        There are two algorithms to generate numbers:
        loop_and_add: Pass in a generic shifted. Checks if a number has been
            calculated. If not, adds them.
        add_from_incomplete_list: generates a list of unknown numbers and adds
            them that way. This algorithm is much faster, especially using small
            batches.
    """
    def __init__(self, last_number=3, step_size=4, batch_value=10000,
                 add_trivial=True):
        # last_number = 3 skips trivial 1 and 2.
        self.last_number = last_number
        # step_size = 4 safely skips 75% of trivial numbers
        self.step_size = step_size
        # Initializes dictionary where EvenSteps objects will be stored.
        self.even_steps = {}
        self.num_even_steps = 0
        # Number of numbers to calculate since last number.
        self.batch_value = batch_value
        # Total percent of all numbers covered
        self.total_percent = 0.0
        # Adds trivial even steps, their remainders and sequences
        if add_trivial:
            # even steps = 1
            even_1 = self.add_even_steps(1, 0)
            even_1.add_remainder(0, '0')

            # even steps = 2
            even_2 = self.add_even_steps(2, 1)
            even_2.add_remainder(1, '100')

    def get_even_steps_list(self):
        """ Returns the sorted keys of the even steps dictionary.

        :return:
        """
        return sorted(self.even_steps.keys())

    def get_num_even_steps(self):
        """ Returns the number of EvenSteps objects.

        :return:
        """
        return self.num_even_steps

    def get_even_steps_object(self, even_steps):
        """ Returns the EvenSteps object associated with the even steps.

        :param even_steps:
        :return:
        """
        assert even_steps in self.get_even_steps_list(), "not in EvenSteps list"
        return self.even_steps[even_steps]

    def get_last_number(self):
        """ Returns the last number calculated in the shifted.

        :return:
        """
        return self.last_number

    def get_all_even_steps_objects(self):
        """ Returns all EvenSteps objects in sorted order.

        :return:
        """
        even_steps_objects = []
        even_steps_list = self.get_even_steps_list()
        for even_steps_num in even_steps_list:
            even_steps_objects.append(self.even_steps[even_steps_num])
        return even_steps_objects

    def add_even_steps(self, even_steps, odd_steps):
        """ Creates a EvenSteps object and stores it in the dictionary.

        :param even_steps:
        :param odd_steps:
        :return:
        """
        assert even_steps not in self.get_even_steps_list(), \
            "already in list"
        even_steps_obj = EvenSteps(even_steps, odd_steps)
        self.even_steps[even_steps] = even_steps_obj
        self.num_even_steps += 1
        return even_steps_obj

    def get_all_remainders(self):
        """Returns all remainders as a giant array.

        :return:
        """
        # Gets all even steps
        even_steps_objects = self.get_all_even_steps_objects()
        # Will be a list of lists that needs flattening
        remainder_temp = []
        for even_steps_obj in even_steps_objects:
            remainder_list = even_steps_obj.get_remainder_list()
            remainder_temp.append(remainder_list)
        # Flattens the list of lists. Recipe stolen from StackExchange.
        remainders = [val for sublist in remainder_temp for val in sublist]
        return remainders

    def get_all_remainder_pairs(self):
        """ Returns all RemainderPair objects.

            There used to be a get all pair sequences method, but you can get
            them yourself using this.

        :return:
        """
        # Will be a list of lists that needs flattening
        remainder_pairs = []
        even_steps_objects = self.get_all_even_steps_objects()
        for even_steps_obj in even_steps_objects:
            pairs = even_steps_obj.get_remainder_pairs()
            if not pairs:
                continue
            remainder_pairs.append(pairs)
        # Flattens the list of lists. Recipe stolen from StackExchange.
        pairs = [val for sublist in remainder_pairs for val in sublist]
        return pairs

    def check_for_number_completeness(self, num):
        """ Checks if an integer exists after the following equation:
            possible_int = (num - remainder)/2 ** even_20

        :param num:
        :return:
        """
        # Converts to float for future calculations
        num = float(num)
        even_steps_list = self.get_even_steps_list()
        for even_steps in even_steps_list:
            even_steps_object = self.get_even_steps_object(even_steps)
            remainders = even_steps_object.get_remainder_list()
            # Performs the above equation then mods it with 1
            possible_ints = [((num - rem) / 2 ** even_steps) % 1
                             for rem in remainders]
            # If there are any zeros, then the number is complete.
            if 0.0 in possible_ints:
                return True
        # Returns false if it makes it through the for loop.
        else:
            return False

    def loop_and_add(self, loop_sequence):
        """ Loops through a shifted, skipping complete numbers, then adds
            incomplete numbers to the dictionary.

        :param loop_sequence:
        :return:
        """
        for num in loop_sequence:
            # first checks if we can calculate it already. If so, continue
            if self.check_for_number_completeness(num):
                continue
            collatz_sequence, parity_sequence, even_steps, \
                remainder = self.calc(num, return_more=True, next_lowest=True)
            even_steps_list = self.get_even_steps_list()
            # even steps already found
            if even_steps in even_steps_list:
                even_steps_object = self.get_even_steps_object(even_steps)
            # new even steps
            else:
                odd_steps = len(parity_sequence) - even_steps
                even_steps_object = self.add_even_steps(even_steps, odd_steps)
            even_steps_object.add_remainder(remainder, parity_sequence)
        self.last_number = loop_sequence[-1]

    def add_from_incomplete_list(self, incomplete_sequence):
        """ This algorithm takes in a list of incomplete numbers and add them.

            Use self.generate_incomplete_numbers() to get a shifted.
            If a new remainder is discovered, it checks if any numbers related
            to that remainder is in the list and removes it if so.

        :param incomplete_sequence:
        :return:
        """
        last_num = incomplete_sequence[-1]
        # The shifted might shorten, so this acts as a shrinking for loop
        index = 0
        while index < len(incomplete_sequence):
            # self.last_number = incomplete_sequence[index]
            collatz_sequence, parity_sequence, even_steps, \
                remainder = self.calc(incomplete_sequence[index],
                                      return_more=True, next_lowest=True)
            even_steps_list = self.get_even_steps_list()
            # even_20 already found
            if even_steps in even_steps_list:
                even_steps_object = self.get_even_steps_object(even_steps)
            # new even steps
            else:
                odd_steps = len(parity_sequence) - even_steps
                even_steps_object = self.add_even_steps(even_steps, odd_steps)
            even_steps_object.add_remainder(remainder, parity_sequence)
            # Checks if there's at least one now known number in the shifted
            if remainder + even_steps < last_num:
                # Presumes first multiple corresponds to remainder, equals 0.
                last_multiple = math.floor((last_num-remainder)/2**even_steps)
                # The next multiple will be 1, so start there.
                multiples = range(1, int(last_multiple + 1))
                # Remove all now known numbers from the shifted
                for multi in multiples:
                    incomplete_sequence.remove(multi*2**even_steps+remainder)
            index += 1

    def add_incomplete_batch(self):
        """ Adds a batch using the "incomplete" algorithm.

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

    def add_batch(self):
        """ Sets a shifted based on the last number and batch value
            and runs it through loop_and_add.

        :return:
        """
        target_num = self.last_number + self.batch_value
        # Adds one to target number for inclusiveness
        sequence = range(self.last_number, target_num + 1, self.step_size)
        self.loop_and_add(sequence)
        # After the batch, check if any new even steps has been completed
        self.check_for_even_steps_completeness()

    def calculate_number_percentage(self):
        """ Calculates how many numbers are covered by the current dictionary.

        The percent that a even steps covers is num_remainders/2**even steps.
        Sum them to get a total percentage of numbers covered.

        :return:
        """
        # TODO: run this every time a new even steps or remainder is added?
        even_steps_objects = self.get_all_even_steps_objects()
        for even_steps_obj in even_steps_objects:
            even_steps = even_steps_obj.get_even_steps()
            remainders = even_steps_obj.get_remainder_list()
            # Needs to be a float or python rounds
            num_remainders = float(len(remainders))
            # Adds the percentage for that even steps.
            self.total_percent += num_remainders / 2 ** even_steps
        return self.total_percent

    def get_all_alphas(self):
        """ Returns all alphas from EvenSteps objects.

        :return:
        """
        alphas = []
        even_steps_objects = self.get_all_even_steps_objects()
        for even_steps_obj in even_steps_objects:
            alphas.append(even_steps_obj.get_alpha())
        return alphas

    def get_incomplete_even_steps(self):
        """ Returns all EvenSteps objects that are not complete.

        :return:
        """
        incomplete_even_steps = []
        even_steps_objects = self.get_all_even_steps_objects()
        for even_steps_obj in even_steps_objects:
            if not even_steps_obj.get_completed():
                incomplete_even_steps.append(even_steps_obj)
        return incomplete_even_steps

    def check_for_even_steps_completeness(self):
        """ Checks if the last num has exceeded the even steps. Sets complete
            if so.

        :return:
        """
        incomplete_even_steps = self.get_incomplete_even_steps()
        for even_steps_obj in incomplete_even_steps:
            even_steps = 2 ** even_steps_obj.get_even_steps()
            if self.last_number >= even_steps:
                even_steps_obj.set_completed(True)

    def generate_incomplete_numbers(self, sequence):
        """ Generates incomplete numbers based on even steps and remainders.

            Use this shifted in self.add_from_incomplete_list()

            The algorithm solves for multi in num=multi*2^even_20+remainder
            and generates the first and last multiple based on the shifted.
            Then it loops through those multiple and removes them from the list.
        :param sequence:
        :return:
        """
        first_num = float(sequence[0])
        last_num = float(sequence[-1])
        even_steps_objects = self.get_all_even_steps_objects()
        for even_steps_obj in even_steps_objects:
            even_steps = even_steps_obj.get_even_steps()
            if even_steps == 1 or even_steps == 2:
                continue
            remainders = even_steps_obj.get_remainder_list()
            for remainder in remainders:
                # Find the first multiple such that multi*2^even_20+remainder
                # is greater than the first multiple. Same with last multiple
                # except less than last number.
                first_multiple = math.ceil((first_num-remainder)/2**even_steps)
                last_multiple = math.floor((last_num-remainder)/2**even_steps)
                multiples = range(int(first_multiple), int(last_multiple + 1))
                # Add these number to our known list
                for multi in multiples:
                    known_number = multi * 2 ** even_steps + remainder
                    # Remove this number from our shifted
                    sequence.remove(known_number)
        return sequence

    @staticmethod
    def calc(number, next_lowest=False, return_more=False):
        """ Calculates the collatz shifted, parity shifted, even steps,
            and the remainder.

        :param number:
        :return:
        """
        if next_lowest:
            target_num = number
        else:
            # Will stop at 1
            target_num = 2
        first = number
        collatz_sequence = [number]
        parity_sequence = ''
        # loops under number is less than first
        while number >= target_num:
            parity = number % 2
            # Odd step
            if parity:
                number = 3 * number + 1
                # parity_sequence += '0'
            # Even step
            else:
                number /= 2
                # parity_sequence += '1'
            collatz_sequence.append(number)
            parity_sequence += str(parity)
        # print parity_sequence
        even_steps = parity_sequence.count('0')
        remainder = first % (2 ** even_steps)
        if return_more:
            return collatz_sequence, parity_sequence, even_steps, remainder
        else:
            return collatz_sequence
