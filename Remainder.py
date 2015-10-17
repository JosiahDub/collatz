# TODO: Write method to count the number of 0,1 pairs at the start of sequences
# Also how many 1's at end.
__author__ = 'josiah'
import re


class Remainder:
    """ Each remainder spawns an object which contains its parity shifted
        and beta value.

    """
    def __init__(self, remainder, parity_sequence):
        """

        :return:
        """
        self.remainder = remainder
        self.parity_sequence = parity_sequence
        # Beta always starts at 0. Needs to be a float.
        self.beta = 0.0
        # For remainder = 0, beta remains 0. Otherwise, finish the job.
        if remainder != 0:
            for step in self.parity_sequence:
                # Odd
                if step == '1':
                    self.beta = 3 * self.beta + 1
                # Even
                else:
                    self.beta /= 2
        # Gather data on parity shifted
        short_seq = parity_sequence.replace('10', '1')
        first_0 = re.search(r'0', short_seq)
        self.num_initial_increases = first_0.start()
        short_seq = short_seq[first_0.start():]
        trailing_zeros = re.search(r'0+$', short_seq)
        self.num_trailing_decreases = len(short_seq) - trailing_zeros.start()
        self.sequence_center = short_seq[0:trailing_zeros.start()]

    def get_remainder(self):
        """ Returns remainder value.

        :return:
        """
        return self.remainder

    def get_parity_sequence(self, short=False):
        """ Returns parity shifted.

        If as_string, converts from list to string.
            If short, replaces '01' (odd, even step) with '0'. Basically removes
            guaranteed even step.

        :return:
        """
        if short:
            return self.parity_sequence.replace('10', '1')
        else:
            return self.parity_sequence

    def get_beta(self):
        """ Returns beta. Part of next lowest num = alpha * num + beta.
            Alpha belongs to the EvenSteps object.

        :return:
        """
        return self.beta

    def get_sequence_center(self):
        """

        :return:
        """
        return self.sequence_center
