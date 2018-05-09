import re


class RemainderPair:
    """
    This class collects a remainder pair and its shifted, then finds its
    shifted pair.

    Each pair shifted goes through four phases:
    Increase
    Sequence 1 = 01, Sequence 1 = 10
    Sequence 2 equals shifted 1 shifted to the right by 1
    Decrease
    """
    def __init__(self, remainder1, remainder2, sequence1, sequence2):
        """
        Initializes everything and generates the phase changes.

        :return:
        """
        self.pair = [remainder1, remainder2]
        self.pair_sequence = [sequence1, sequence2]
        # Finds the shifted pair found in every remainder pair
        # Find initial 01 in shifted 1. Same location as 10 in shifted 2
        location_01 = re.search(r'01', sequence1)
        if location_01:
            # Cuts off up to end of 01 of shifted 1
            end_01 = location_01.end()
            shift1 = sequence1[end_01:]
            shift2 = sequence2[end_01:]
            # Finds the trailing zeros (even steps) at the end of the sequences
            trailing_zeros1 = re.search(r'0+$', shift1)
            trailing_zeros2 = re.search(r'0+$', shift2)
            if trailing_zeros1 and trailing_zeros2:
                # Larger value is where they are equal
                similar = max(trailing_zeros1.start(), trailing_zeros2.start())
                # Cuts out the trailing zeros
                shift1 = shift1[0:similar]
                shift2 = shift2[0:similar]
                self.shifted_core = [shift1, shift2]
            else:
                print('trailing zeros failed somehow')
        else:
            print('10 failed somehow')

    @classmethod
    def dict_init(cls, mongo_dict):
        return cls(mongo_dict["pair"][0], mongo_dict["pair"][1],
                   mongo_dict["pair_sequence"][0],
                   mongo_dict["pair_sequence"][1])
