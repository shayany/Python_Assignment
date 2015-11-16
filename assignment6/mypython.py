#!/usr/bin/env python
# encoding: utf-8

"""Small script for controlling charactor input in more detail.

To explore what key results in what output, use it interactively.
For example:

    $ ./getchar.py
    prompt:å
    repr:"\xc3\xa5"

Can also be evoced through python import.
For example, for the same special character:

    >>> import getchar
    >>> getchar.getchar()
    <<< '\xc3'
    >>>

Note that the characters that spans multiple bytes, only first character is
returned.  The rest has to be retrieve the manually. For example for 'å':

    >>> import sys
    >>> print sys.stdout.read(1)
    '\xa5'
"""

import tty, sys
from feedline import feedline
def isAlphaNumericSymbol(ch):
    return ord(ch) in range(32,128)
# windows implementation
try:

    import msvcrt

    def getchar():
        return msvcrt.getch()

# unix/mac implementation
except:

    import termios

    def getchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


if __name__ == "__main__":
    lineNumber=0
    localNamespace=vars().copy()
    print "Welcome to Shayan IPython"
    while True:
        sys.stdout.write("in [{0}] :".format(lineNumber))
        lineNumber+=1
        lineLen=0
        codeLen=0
        cursorPosition=0
        line = ""
        code = ""
        while True:        
            char = getchar()
            lineLen+=1        
            if char in '[O' and line[lineLen-2:] == "\x1b":
                pass
            elif char=='A' and line[lineLen-3:] == "\x1b[":
                sys.stdout.write("up")
            elif char=='B' and line[lineLen-3:] == "\x1b[":
                sys.stdout.write("down")
            elif char=='C' and line[lineLen-3:] == "\x1b[":
                if(cursorPosition<codeLen):
                    sys.stdout.write("\x1b[C")
                    cursorPosition+=1                    
                #sys.stdout.write("Right")
            elif char=='D' and line[lineLen-3:] == "\x1b[":
                if(cursorPosition>0):
                    sys.stdout.write("\x1b[D")
                    cursorPosition-=1
                #sys.stdout.write("Left")
            elif char=='H' and line[lineLen-3:] == "\x1bO":
                sys.stdout.write("Home")
            elif char=='F' and line[lineLen-3:] == "\x1bO":
                sys.stdout.write("End")
            elif char=="\x7f":                                        
                sys.stdout.write("Backspace")           
            elif char=='~' and line[lineLen-4:] == "\x1b[2":
                sys.stdout.write("insert")
            elif char=='~' and line[lineLen-4:] == "\x1b[3":
                sys.stdout.write("Delete") 
            elif char=='~' and line[lineLen-4:] == "\x1b[5":
                sys.stdout.write("Page Up")
            elif char=='~' and line[lineLen-4:] == "\x1b[6":
                sys.stdout.write("Page Down")
            elif isAlphaNumericSymbol(char):
                code+=char
                codeLen+=1
                cursorPosition+=1                                                  
                sys.stdout.write(char)               
            elif char=="\x04":
                if code:
                    sys.stdout.write("\n")
                    lineNumber-=1
                    break
                else:
                    sys.stdout.write("\n Thanks! \n")
                    sys.exit(0)                
            # stop cycle
            if char in "\r\n":
                # write repr of character for testing purposes                
                if not line:
                    #sys.stdout.write("repr newline:" + repr(char) + "\n")
                    sys.stdout.write("\n")
                    print feedline(code,localNamespace)                    
                else:
                    #sys.stdout.write("\nrepr:" + repr(line) + "\n")
                    sys.stdout.write("\n")
                    print feedline(code,localNamespace)                    
                #sys.exit(0)
                break;
                    
            # add char to line
            line+=char