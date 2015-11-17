import sys
from StringIO import StringIO
import traceback

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

    # Swap stdout with a StringIO instance
    oldio, sys.stdout = sys.stdout, StringIO()
    try:
        try:
            eval(code, namespace)
        except:
            exec(code, namespace)                            
    except Exception as error:
        # Get stdout buffer
        out = sys.stdout.getvalue()
        sys.stdout = oldio
        return "Error: {0}".format(error)#Return a decription of error
    # Get stdout buffer
    out = sys.stdout.getvalue()
    # Reset stdout
    sys.stdout = oldio
    # Print out captured stdout
    return out[:-1]
