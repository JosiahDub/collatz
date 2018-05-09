from Collatz import *

collatz = Collatz()
# Fastest way to calculate new numbers, compared to collatz.add_batch()
collatz.add_incomplete_batch()
# Gives a list of all unique e.
print("even steps: ", collatz.even_steps.keys())
even_20 = collatz.even_steps[20]
# Gives a list of all unique r for that e.
# May not be a complete list depending on how high we calculated
print "remainders: ", even_20.remainders.keys()
print "***** Remainder example *****"
remainder_1127 = even_20.remainders[1127]
print "Parity shifted: ", remainder_1127.sequence
# Isolates the "center",
# i.e. the value between initial increases and final decreases
print 'Parity core: ', remainder_1127.sequence_center
# Gets a list of RemainderPair objects
print "***** Remainder pair example ******"
remainder_pairs = even_20.remainder_pairs
pair = remainder_pairs[0].pair
print 'Remainder pair: '
print pair[0]
print pair[1]
# short=True replaces (odd, even) steps with just odd.
# Makes patterns more obvious.
sequence = remainder_pairs[0].pair_sequence
print 'Pair sequence: '
print sequence[0]
print sequence[1]
# Shifted pair is shortened by default
shifted = remainder_pairs[0].shifted_core
print 'Shifted pair: '
print shifted[0]
print shifted[1]
