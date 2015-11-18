# File: my_webserver.py
from flask import Flask,render_template,request
from feedline import feedline

lineNumber=0
namespace=vars().copy()

app = Flask(__name__)

@app.route("/")
def home():
    namespace['lineNumber']=0
    return render_template('shell.html',pythonCommand="") 
       
@app.route("/handle_python_commands",methods=['POST'])
def shellInterpreter():
    assert request.method == 'POST'
    pythonCommand = request.form["pythonCommand"]    
    try:
        terminal=request.form["terminal"]
        terminal+=pythonCommand+"\r\n"+feedline(pythonCommand,namespace)
    except:
        terminal="In [0]: "+pythonCommand+"\r\n"+feedline(pythonCommand,namespace)
    return render_template('shell.html',result=terminal)
    
if __name__=="__main__":
    app.run()