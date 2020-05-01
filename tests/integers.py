from testlib import validator

N = 100000

test_string = " ".join(map(str,range(N)))
v = validator(test_string)
assert(v.readInts(N) == list(range(N)))