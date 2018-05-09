class EvenSteps:
    """
    Each Even Step has its own object.

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
        # Completed is if the sequence has calculated beyond 2 ** even steps
        self.completed = False
        # Calculates alpha = 3^odd_steps/2^even_steps
        # Part of the equation: next lowest num = alpha * num + beta.
        # Beta is owned by the specific remainder and differs based on sequence
        self.alpha = 3.0 ** self.odd_steps / 2.0 ** self.even_steps

    @classmethod
    def dict_init(cls, even_dict):
        even = cls(even_dict['even'], even_dict['odd'])
        even.completed = even_dict['completed']
        return even
