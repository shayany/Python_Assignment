import sys
from StringIO import StringIO
import traceback

def feedline(code,namespace):
    # Swap stdout with a StringIO instance
    oldio, sys.stdout = sys.stdout, StringIO()
    try:
        try:
            eval(code, namespace)
        except:
            exec(code, namespace)        
        # Get stdout buffer
    except Exception as error:
        out = sys.stdout.getvalue()
        sys.stdout = oldio
        return "Error: {0}".format(error)
    out = sys.stdout.getvalue()
    # Reset stdout
    sys.stdout = oldio
    # Print out captured stdout
    return out
