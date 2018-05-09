import re
# TODO: Write method to count the number of 0,1 pairs at the start of sequences
# Also how many 1's at end.


class Remainder:
    """
    Each remainder spawns an object which contains its parity shifted
    and beta value.

    """
    def __init__(self, remainder, sequence):
        """

        :return:
        """
        self.remainder = remainder
        self.sequence = sequence
        # Beta always starts at 0. Needs to be a float.
        self.beta = 0.0
        # For remainder = 0, beta remains 0. Otherwise, finish the job.
        if remainder != 0:
            for step in self.sequence:
                # Odd
                if step == '1':
                    self.beta = (3 * self.beta + 1) / 2
                # Even
                else:
                    self.beta /= 2
        # Gather data on parity shifted
        first_0 = re.search(r'0', sequence)
        self.num_initial_increases = first_0.start()
        # Everything from the first zero to the end
        zero_to_end = sequence[first_0.start():]
        # All of the last zeros
        trailing_zeros = re.search(r'0+$', zero_to_end)
        self.num_trailing_decreases = len(zero_to_end) - trailing_zeros.start()
        self.sequence_center = zero_to_end[0:trailing_zeros.start()]

    @classmethod
    def dict_init(cls, mongo_dict):
        return cls(mongo_dict["remainder"], mongo_dict["sequence"])
