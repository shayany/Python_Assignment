import sys
from StringIO import StringIO
namespace = vars().copy()
code = """
import random
print "hello world"
"""
# Swap stdout with a StringIO instance
oldio, sys.stdout = sys.stdout, StringIO()
exec(code, namespace)
# Get stdout buffer
out = sys.stdout.getvalue()
# Reset stdout
sys.stdout = oldio
# Print out captured stdout
print out