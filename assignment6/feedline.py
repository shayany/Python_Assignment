import sys
from StringIO import StringIO
import traceback
from re import *
#lineNumber should be provided in namespace
#lineNumber=0
#n=vars().copy() 

def feedline(code,namespace):
    """Execute the python command and return the result

    Args:        
        code (str): line of python code
        namespace (list): list of all the variables in the current namespace
    Returns:
        result of the commands
    Raises:
        In case of exception it returns a description of the error

    """
    commandResult=""

    if code.strip()!="":
        namespace['lineNumber']+=1       

    # Swap stdout with a StringIO instance
    oldio, sys.stdout = sys.stdout, StringIO()

    try:
        try:
            commandResult=eval(code, namespace)
        except:
            exec(code, namespace)                            
    except Exception as error:
        # Get stdout buffer
        out = sys.stdout.getvalue()
        sys.stdout = oldio
        return "Error: {0}\r\nIn [{1}]: ".format(error,namespace['lineNumber'])#Return a decription of error

    # Get stdout buffer
    out = sys.stdout.getvalue()
    # Reset stdout
    sys.stdout = oldio
    
    #return out[:-1]
    if commandResult:
        out+=str(commandResult)+"\r\n"
    if "print" not in code:                    
        if out:
            out="Out[{0}]: {1}".format(namespace['lineNumber']-1,out)
    return out+"In [{0}]: ".format(namespace['lineNumber'])

