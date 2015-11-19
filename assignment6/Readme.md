Before running the feedline function you have to added these two lines before the function.

```python
lineNumber=0
namespace=vars().copy()
```

###Example of running feedline in IPython:


```python
lineNumber=0
namespace=vars().copy()
from feedline import feedline
print feedline("print 'Hello World!'",namespace)
print feedline("",namespace)
print feedline("x = 1",namespace)
print feedline("x += 1",namespace)
print repr(feedline("print x",namespace))
print feedline("from math import sin",namespace)
print feedline("def f(x): return sin(x**2)",namespace)
print feedline("f(x)",namespace)
```


###Web interface:

Before using the web interface you have to activate the server.	

```shell
python my_webserver.py
```	
	
