#!/usr/bin/env python
# encoding: utf-8

import os
from feedline import feedline
from oscommands import *
from helpcommands import *
from savecommand import *
from getchar import *



def clearLine():
    """clear the current line in terminal
    """
    rows, columns = os.popen('stty size', 'r').read().split() #Return size of terminal window
    sys.stdout.flush()
    temp=""
    for i in range(int(columns)):# Create an empty line 
        temp+=' '                                                
    sys.stdout.write("\r"+temp)  #Write an empty line and carriage return 
          
          
          
def isAlphaNumericSymbol(ch):
    """Check wether the character is non-control(printable) or not
    Args:        
        ch (char): single character
    Returns:
        True : If non-control(printable)
    
    """
    return ord(ch) in range(32,128)
    
    
    
if __name__ == "__main__":
    lineNumber=0            #This variable keeps prompt's line number
    localNamespace=vars().copy()    #Saving a namespace 
    
    print "Welcome to Shayan IPython"
    
    commandHistory=[]            #List of all commands which has been executed
    commandHistoryPointer=0      #Pointor to the the commandHistory (When we press up and down button it will be changed accordingly)
    sys.stdout.write("In [{0}]: ".format(lineNumber))
    while True:
        #sys.stdout.write("In [{0}]: ".format(lineNumber))        
        lineNumber+=1
        
        line = ""
        lineLen=0        #Lenght of line which contains all the characters (ASCII) 
        
        code = ""        #code is an input for feedline function 
        codeLen=0        #Lenght of the command which has will be typed by user (Only printable Characters)
        
        cursorPosition=0 #Pointer to the position of cursor on terminal
                   
        while True:     
            char = getchar()
            lineLen+=1 #It will be increased when we start a new line         
            
            
            if char in '[O' and line[lineLen-2:] == "\x1b":
                pass        #Check control characters (All control character has the same prefix)

            elif char=="\t":
                #Check the the character is tab or not                
                #sys.stdout.write("TAB")
                if code:
                    temp=""
                    similar=0                
                    for command in localNamespace:#find all the variables with same prefix with current commands
                        if code == command[:len(code)]:
                            temp+=command+"\t"
                            similar+=1
                    if similar>1:#If there are many variables with same prefix shows all of them to user
                        clearLine()
                        sys.stdout.write('\rIn [{0}]: {1}'.format(lineNumber-1,code))
                        sys.stdout.write("\n"+temp+"\n")
                        sys.stdout.write('\rIn [{0}]: '.format(lineNumber-1))
                        lineNumber-=1#In case of tab completion line number should not increase                   
                        break
                    elif similar==1:
                        clearLine()#If there is only one variable with same prefix complete the name in same line
                        sys.stdout.write('\rIn [{0}]: {1}'.format(lineNumber-1,temp[:-1]))
                        code=temp[:-1]                    
            elif char=='B' and line[lineLen-3:] == "\x1b[":
                #If user press the down arrow key show the next command from the commands history(All commands)
                if(commandHistoryPointer<len(commandHistory)-1):
                    commandHistoryPointer+=1
                    clearLine()
                    sys.stdout.write('\rIn [{0}]: '.format(lineNumber-1))
                    sys.stdout.write(commandHistory[commandHistoryPointer])
                    code=commandHistory[commandHistoryPointer]
            elif char=='A' and line[lineLen-3:] == "\x1b[":
                #If user press the up arrow key show the previous command from the commands history(All commands)
                if(commandHistoryPointer>0):
                    commandHistoryPointer-=1
                    clearLine()
                    sys.stdout.write('\rIn [{0}]: '.format(lineNumber-1))
                    sys.stdout.write(commandHistory[commandHistoryPointer])
                    code=commandHistory[commandHistoryPointer]                                  
            elif char=='C' and line[lineLen-3:] == "\x1b[":
                #It's not part of assignment (right arrow key)
                if(cursorPosition<codeLen):
                    sys.stdout.write("\x1b[C")
                    cursorPosition+=1                    
                #sys.stdout.write("Right")
            elif char=='D' and line[lineLen-3:] == "\x1b[":
                #It's not part of assignment (left arrow key)        
                if(cursorPosition>0):
                    sys.stdout.write("\x1b[D")
                    cursorPosition-=1
                #sys.stdout.write("Left")
            elif char=='H' and line[lineLen-3:] == "\x1bO":
                #It's not part of assignment (Home key)
                #sys.stdout.write("Home")
                pass
            elif char=='F' and line[lineLen-3:] == "\x1bO":
                #It's not part of assignment (End key)
                #sys.stdout.write("End")
                pass
            elif char=="\x7f":                                        
                #If backspace will be press , cursor goes to the previous position and write space and goes back again
                if len(code)>0:
                    sys.stdout.write("\x1b[D")           
                    sys.stdout.write(" ")
                    sys.stdout.write("\x1b[D")
                    code=code[:-1]    #Update the code 
            elif char=='~' and line[lineLen-4:] == "\x1b[2":
                #It's not part of assignment (insert key)
                #sys.stdout.write("insert")
                pass
            elif char=='~' and line[lineLen-4:] == "\x1b[3":
                #It's not part of assignment (Delete key)
                #sys.stdout.write("Delete")
                pass 
            elif char=='~' and line[lineLen-4:] == "\x1b[5":
                #It's not part of assignment (Page Up key)
                #sys.stdout.write("Page Up")
                pass
            elif char=='~' and line[lineLen-4:] == "\x1b[6":
                #It's not part of assignment (Page Down key)
                #sys.stdout.write("Page Down")
                pass
            elif isAlphaNumericSymbol(char):#If character is printable(not control),it will be added to code
                code+=char
                codeLen+=1
                cursorPosition+=1                                                  
                sys.stdout.write(char)               
            elif char=="\x04":#If CTRL+D will be pressed
                if code:      #Empty the buffer
                    sys.stdout.write("\r\nKeyboardInterupt\n")
                    sys.stdout.write("In [{0}]: ".format(lineNumber-1))
                    lineNumber-=1#Program should not increase the prompt line number
                    break
                else:         #Exit from the program
                    sys.stdout.write("\nThanks! \n")
                    sys.exit(0)                
            # stop cycle
            if char in "\r\n":
                #If user press the enter (based on the OS)
                if code=="":#program should not increase the number line when we enter empty command
                    lineNumber-=1
                    sys.stdout.write("\r\nIn [{0}]: ".format(lineNumber))
                    break                
                if not line:
                    sys.stdout.write("\n")
                    commandHistory.append(code)
                    commandHistoryPointer=len(commandHistory)-1
                    commandHistoryPointer+=1
                    if code:# Check type of the commands
                        if(code[0]=="!"):#Operating system commands
                            sys.stdout.write(OS_Commands(code))
                            sys.stdout.write("In [{0}]: ".format(lineNumber))
                        elif(code[-1]=="?"):#Helper commands
                            helpCommands(code)
                            sys.stdout.write("In [{0}]: ".format(lineNumber))
                        elif(code[:5]=="%save"):#Save command history
                            saveCommandsHistory(commandHistory,code.split()[1])                                                                                    
                            sys.stdout.write("In [{0}]: ".format(lineNumber))
                        else:
                            sys.stdout.write(feedline(code,localNamespace)) 
                else:
                    sys.stdout.write("\n")
                    commandHistory.append(code)
                    commandHistoryPointer=len(commandHistory)-1
                    commandHistoryPointer+=1
                    if code:# Check type of the commands
                        if(code[0]=="!"):#Operating system commands
                            sys.stdout.write(OS_Commands(code))
                            sys.stdout.write("In [{0}]: ".format(lineNumber))
                        elif(code[-1]=="?"):#Helper commands
                            helpCommands(code)
                            sys.stdout.write("In [{0}]: ".format(lineNumber))
                        elif(code[:5]=="%save"):#Save command history
                            saveCommandsHistory(commandHistory,code.split()[1])                                                                                    
                            sys.stdout.write("In [{0}]: ".format(lineNumber))
                        else:
                            sys.stdout.write(feedline(code,localNamespace))                                        
                break;                    
            # add char to line
            line+=char
