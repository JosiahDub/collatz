from pymongo import MongoClient
from CollatzContainer import CollatzContainer


class CollatzMongo(CollatzContainer):
    def __init__(self):
        super().__init__()
        self.mongo = MongoClient('localhost', 27017)
        self.database = self.mongo.get_database('collatz')
        self.even = self.database.get_collection('even')
        self.remainder = self.database.get_collection("remainders")
        self.pair = self.database.get_collection("pairs")
        self.stats = self.database.get_collection('stats')

    # ########################
    # EVEN
    # ########################

    def add_even(self, even):
        document = {'even': even.even_steps, 'odd': even.odd_steps,
                    'completed': False, 'alpha': even.alpha}
        self.even.insert_one(document)

    def even_exists(self, even):
        return self.even.find_one({"even": even}) is not None

    def even_complete(self, even):
        even = self.even.find_one({"even": even})
        return even["completed"]

    def set_even_completeness(self, even, complete):
        self.even.update_one({"even": even},
                             {"$set": {"completed": complete}})

    def get_even_list(self):
        evens = []
        for doc in self.even.find({}, {"even": 1, "_id": 0}):
            evens.append(doc["even"])
        return evens

    def get_complete_evens(self, complete):
        evens = []
        for doc in self.even.find({"completed": complete},
                                  {"even": 1, "_id": 0}):
            evens.append(doc["even"])
        return evens

    # ######################
    # REMAINDER
    # ######################

    def add_remainder(self, even, rem):
        remainder_doc = {"remainder": rem.remainder,
                         "even": even,
                         'sequence': rem.sequence,
                         'beta': rem.beta,
                         'num_initial_increases': rem.num_initial_increases,
                         'num_trailing_decreases': rem.num_trailing_decreases,
                         'sequence_center': rem.sequence_center}
        self.remainder.insert_one(remainder_doc)

    def add_remainder_pair(self, even, pair):
        pair_doc = {'pair': pair.pair, "even": even,
                    'shifted_core': pair.shifted_core}
        self.pair.insert_one(pair_doc)

    def remainder_exists(self, even, rem):
        return self.remainder.find_one({"even": even, "remainder": rem}) is not None

    def get_num_remainders(self, even):
        return self.remainder.find({"even": even}).count()

    def get_remainder_pair_sequence(self, pair):
        pair_sequence = []
        first_doc = self.remainder.find_one({"remainder": pair[0]},
                                            {"sequence": 1, "_id": 0})
        pair_sequence.append(first_doc["sequence"])
        second_doc = self.remainder.find_one({"remainder": pair[1]},
                                             {"sequence": 1, "_id": 0})
        pair_sequence.append(second_doc["sequence"])
        return pair_sequence

    def get_even_remainders(self, even):
        remainders = []
        for doc in self.remainder.find({"even": even}, {"_id": 0, "remainder": 1}):
            remainders.append(doc["remainder"])
        return remainders

    def get_sequence(self, remainder):
        rem_doc = self.remainder.find_one({"remainder": remainder},
                                          {"_id": 0, "sequence": 1})
        return rem_doc["sequence"]

    # #####################################
    # STATS
    # #####################################

    def update_last_number(self, number):
        self.stats.update_one({}, {'$set': {'last_number': number}})

    def get_last_number(self):
        return self.stats.find_one({})["last_number"]

    def update_percent_complete(self, percent):
        self.stats.update_one({}, {'$set': {'percent_complete': percent}})

    def get_stats(self):
        return self.stats.find_one({}, {"_id": 0})

    def get_continue(self):
        doc = self.stats.find_one({}, {"_id": 0, "continue": 1})
        return doc["continue"]

    def set_continue(self, continuing):
        self.stats.update_one({}, {"$set": {"continue": continuing}})
