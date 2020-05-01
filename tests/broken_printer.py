from testlib import validator

testInput = \
"""5 15
1FFRBBRFF0ULB10

   """
v = validator(testInput)
N = v.readInt(1,1000)
v.readSpace()
M = v.readInt(2,1000000)
v.readEoln()
cmds = v.readLine("[FBLRU01]*0$")
assert(len(cmds)==M)
v.strict = False
v.readEOF()