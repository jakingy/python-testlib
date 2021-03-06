import sys
import re
import string

LF = '\n'
CR = '\r'
SPACE = ' '
TAB = '\t'
EOLNS = "\n\r"
WHITESPACES = " \t" + EOLNS

intregex = r"^-?[1-9]\d*|0$"
intpattern = re.compile(intregex)

def strictInt(x: str, lo=None, hi=None) -> int:
    res = int(x)
    if not intpattern.match(x):
        raise Exception("Invalid integer")
    if lo is not None and res < lo:
        raise Exception("Integer less than lo bound")
    if hi is not None and res > hi:
        raise Exception("Integer greater than hi bound")
    return res

def isBlank(c):
    return c in WHITESPACES

def isEoln(c):
    return c in EOLNS

class validator:
    def __init__(self, string=None, strict=True):
        self.idx = 0
        if string is None:
            string = sys.stdin.read()
        self.string = string
        self.strict = strict

    def peekChar(self):
        if self.idx == len(self.string):
            raise Exception("Unexpected EOF")
        return self.string[self.idx]

    def readChar(self, c=None):
        ch = self.peekChar()
        if c is not None and ch!=c:
            raise  Exception("Unexpected character") 
        self.idx += 1
        return ch

    def readOptional(self, c):
        try:self.readChar(c)
        except:pass

    def readSpace(self):
        return self.readChar(' ')

    def unreadChar(self):
        self.idx -= 1

    def skipBlanks(self):
        while not self.isEOF() and isBlank(self.peekChar()):
            self.idx += 1

    def readUntil(self, endF, regex=None):
        chars = []
        c = self.peekChar()
        if endF(c):
            raise Exception("Unexpected read termination - expected something")
        while not endF(c):
            chars.append(c)
            self.idx += 1
            if self.idx >= len(self.string):
                break
            c = self.peekChar()
        res = ''.join(chars)
        if regex is not None:
            pattern = re.compile(regex)
            if not pattern.match(res):
                raise Exception("Result does not match pattern")
        return res

    def readToken(self, regex=None):
        if not self.strict:
            self.skipBlanks()
        return self.readUntil(isBlank, regex)

    def readLine(self, regex=None):
        return self.readUntil(isEoln, regex)

    def readString(self, regex=None):
        return self.readLine(regex)

    def readWord(self, regex=None):
        return self.readToken(regex)
        
    def readInt(self, L=None, R=None):
        return strictInt(self.readToken(), L, R)

    def readLong(self, L=None, R=None):
        return self.readInt(L=None, R=None)

    def readInteger(self, L=None, R=None):
        return self.readInt(L=None, R=None)

    def readInts(self, n, L=None, R=None):
        res = []
        if n > 0:res.append(self.readInt(L,R))
        for i in range(1,n):
            self.readSpace()
            res.append(self.readInt(L,R))
        return res

    def readIntegers(self, *args, **kwargs):
        return self.readInts(*args, **kwargs)

    def readLongs(self, *args, **kwargs):
        return self.readInts(*args, **kwargs)

    def readEoln(self):
        if self.string[self.idx]=='\r':
            self.idx += 1
        if self.string[self.idx]!='\n':
            raise Exception("Expected Eoln")
        self.idx += 1

    def isEOF(self):
        return self.idx == len(self.string)

    def readEOF(self):
        if not self.strict:
            self.skipBlanks()            
        if not self.isEOF():
            raise Exception("Expected EOF")
