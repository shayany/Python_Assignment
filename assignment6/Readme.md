Before running the feedline function you have to added these two lines before the function.

Example of running feedline in IPython:

lineNumber=0
namespace=vars().copy()

from feedline import feedline
print feedline("print 'Hello World!'",namespace)



Web interface:

Before using the web interface you have to activate the server.	

python my_webserver.py
	
	
