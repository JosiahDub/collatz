class CollatzContainer:
    """
    A base class to hold Collatz info. Can connect to MongoDB, or simply hold some lists.
    """
    def __init__(self):
        pass

    def add_even(self, even):
        raise NotImplementedError

    def even_exists(self, even):
        raise NotImplementedError

    def even_complete(self, even):
        raise NotImplementedError

    def set_even_completeness(self, even, complete):
        raise NotImplementedError

    def get_even_list(self):
        raise NotImplementedError

    def get_complete_evens(self, complete):
        raise NotImplementedError

    # ######################
    # REMAINDER
    # ######################

    def add_remainder(self, even, rem):
        raise NotImplementedError

    def add_remainder_pair(self, even, pair):
        raise NotImplementedError

    def remainder_exists(self, even, rem):
        raise NotImplementedError

    def get_num_remainders(self, even):
        raise NotImplementedError

    def get_remainder_pair_sequence(self, pair):
        raise NotImplementedError

    def get_even_remainders(self, even):
        raise NotImplementedError

    def get_sequence(self, remainder):
        raise NotImplementedError

    # #####################################
    # STATS
    # #####################################

    def update_last_number(self, number):
        raise NotImplementedError

    def get_last_number(self):
        raise NotImplementedError

    def update_percent_complete(self, percent):
        raise NotImplementedError

    def get_stats(self):
        raise NotImplementedError
