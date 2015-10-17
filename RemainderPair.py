__author__ = 'josiah'
import re


class RemainderPair:
    """ This class collects a remainder pair and its shifted, then finds its
        shifted pair.

        Each pair shifted goes through four phases:
        Increase
        Sequence 1 = 01, Sequence 1 = 10
        Sequence 2 equals shifted 1 shifted to the right by 1
        Decrease
    """
    def __init__(self, remainder1, remainder2, sequence1, sequence2):
        """ Initializes everything and generates the phase changes.

        :return:
        """
        self.remainder_pair = [remainder1, remainder2]
        self.remainder_pair_sequence = [sequence1, sequence2]
        short_seq1 = sequence1.replace('10', '1')
        short_seq2 = sequence2.replace('10', '1')
        # Finds the shifted pair found in every remainder pair
        # Find initial 01 in shifted 1. Same location as 10 in shifted 2
        location_01 = re.search(r'01', short_seq1)
        if location_01:
            # Start of 01 is also how many increases there are
            self.num_initial_increases = location_01.start()
            # Cuts off up to end of 01 of shifted 1
            end_01 = location_01.end()
            shift1 = short_seq1[end_01:]
            shift2 = short_seq2[end_01:]
            # Finds the trailing zeros (even steps) at the end of the sequences
            trailing_zeros1 = re.search(r'0+$', shift1)
            trailing_zeros2 = re.search(r'0+$', shift2)
            if trailing_zeros1 and trailing_zeros2:
                # Larger value is where they are equal
                similar = max(trailing_zeros1.start(), trailing_zeros2.start())
                self.num_trailing_decreases = len(shift1) - similar
                # Cuts out the trailing zeros
                shift1 = shift1[0:similar]
                shift2 = shift2[0:similar]
                self.shifted_pair = [shift1, shift2]
            else:
                'trailing zeros failed somehow'
        else:
            print('10 failed somehow')

    def get_pair(self):
        """ Returns the remainder pair.

        :return:
        """
        return self.remainder_pair

    def get_pair_sequence(self, short=False):
        """ Returns the remainder pair's shifted.

        :return:
        """
        if short:
            short_1 = self.remainder_pair_sequence[0].replace("10", "1")
            short_2 = self.remainder_pair_sequence[1].replace("10", "1")
            return [short_1, short_2]
        return self.remainder_pair_sequence

    def get_shifted_pair(self):
        """ Returns the shifted pair as a list.

        :return:
        """
        return self.shifted_pair

    def get_num_initial_increases(self):
        """ Returns the number of initial increase steps.

        :return:
        """
        return self.num_initial_increases

    def get_num_trailing_decreases(self):
        """ Returns the number of final decrease steps.

        :return:
        """
        return self.num_trailing_decreases
