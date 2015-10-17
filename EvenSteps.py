__author__ = 'josiah'
from Remainder import *
from RemainderPair import *


class EvenSteps:
    """ Each Even Step has its own object.

    This class holds a dictionary of Remainder objects, remainder pairs, alpha.

    Strangely, there are several remainders that come in pairs:
    remainder, 2*remainder+1. This class collects these pairs for ease of use.

    Once a number has been sequenced, the next lowest number can be found by:
    next lowest num = alpha*num + 1. Alpha is based on even/odd steps. Beta is
    based on the specific sequence and is stored in the Remainder object.

    """
    def __init__(self, even_steps, odd_steps):
        """

        :param even_steps:
        :param odd_steps:
        :return:
        """
        self.even_steps = even_steps
        self.odd_steps = odd_steps
        # Initializes remainder dictionary which will store remainder objects.
        self.remainders = {}
        self.num_remainders = 0
        # Initializes list of remainder pairs.
        self.remainder_pairs = []
        # Completed is if the sequence has calculated beyond 2 ** even steps
        self.completed = False
        # Calculates alpha = 3^odd_steps/2^even_steps
        # Part of the equation: next lowest num = alpha * num + beta.
        # Beta is owned by the specific remainder and differs based on sequence
        self.alpha = 3.0 ** self.odd_steps / 2.0 ** self.even_steps

    def get_even_steps(self):
        """ Returns even steps.

        :return:
        """
        return self.even_steps

    def get_odd_steps(self):
        """ Returns odd steps.

        :return:
        """
        return self.odd_steps

    def get_remainder_list(self):
        """ Returns the remainder list, sorted.

        :return:
        """
        return sorted(self.remainders.keys())

    def get_remainder_object(self, remainder):
        """ Returns the remainder object associated with remainder.

        :param remainder
        :return:
        """
        assert remainder in self.get_remainder_list()
        return self.remainders[remainder]

    def add_remainder(self, remainder, parity_sequence):
        """Creates a remainder object, adds it to the list, and checks for a
           pair in the form of (remainder, 2 * remainder + 1).

           If a pair is found, create a RemainderPair object and catalog it.

        :param remainder:
        :param parity_sequence:
        :return:
        """
        assert remainder not in self.get_remainder_list(), \
            "remainder already there"
        remainder_obj = Remainder(remainder, parity_sequence)
        # Add the new object to the dictionary
        self.remainders[remainder] = remainder_obj
        self.num_remainders += 1
        # This assumes that remainders will be found in ascending order.
        if (remainder - 1) / 2 in self.get_remainder_list():
            first_rem = (remainder - 1) / 2
            # Gets the pair's parity sequence
            first_rem_obj = self.get_remainder_object(first_rem)
            first_rem_sequence = first_rem_obj.get_parity_sequence()
            remainder_pair = RemainderPair(first_rem, remainder,
                                           first_rem_sequence, parity_sequence)
            self.remainder_pairs.append(remainder_pair)
        return remainder_obj

    def get_alpha(self):
        """ Returns alpha.

            Part of the equation next lowest num = alpha * num + beta. Betas are
            unique to the Remainder.

        :return:
        """
        return self.alpha

    def get_all_betas(self):
        """ Returns all betas for each remainder.

            Part of the equation next lowest num = alpha * num + beta
        :return:
        """
        betas = []
        remainders = self.get_remainder_list()
        for remainder in remainders:
            remainder_obj = self.get_remainder_object(remainder)
            beta = remainder_obj.get_beta()
            betas.append(beta)
        return betas

    def get_all_parity_sequences(self, short=False):
        """ Returns all of the parity sequences from all Remainder objects.

        If as_string, converts from list to string.
            If short, replaces '01' (odd, even step) with '0'. Basically removes
            guaranteed even step.

        :param short:
        :return:
        """
        sequences = []
        remainders = self.get_remainder_list()
        for remainder in remainders:
            remainder_obj = self.get_remainder_object(remainder)
            sequence = remainder_obj.get_parity_sequence(short=short)
            sequences.append(sequence)
        return sequences

    def get_remainder_pairs(self):
        """ Returns a list of RemainderPair objects.

        :return:
        """
        return self.remainder_pairs

    def set_completed(self, completed):
        """ Sets completed.

        :param completed:
        :return:
        """
        self.completed = completed

    def get_completed(self):
        """ Returns completed status.

        :return:
        """
        return self.completed
