import sys
from StringIO import StringIO
def feedline(code,namespace):
    # Swap stdout with a StringIO instance
    oldio, sys.stdout = sys.stdout, StringIO()
    try:
        eval(code, namespace)
    except:
        exec(code, namespace)        
    # Get stdout buffer
    out = sys.stdout.getvalue()
    # Reset stdout
    sys.stdout = oldio
    # Print out captured stdout
    return out
