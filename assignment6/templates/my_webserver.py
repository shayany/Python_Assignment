# File: my_webserver.py
from flask import Flask,render_template,request

app = Flask(__name__)

users = {"richard": "Richard Lee",
         "john": "John Smith",
         "shayany":"Shayan Yazdanmehr"}

@app.route('/post/')
@app.route('/post/<name>')
def post(name=None):
    return render_template('post.html', fullname=name)

@app.route('/login')
def login():
    return render_template('login.html')    

@app.route('/handle_login', methods=['POST'])                                                                                                                                                                                                  
def handle_login():           
    
    assert request.method == 'POST'   # Check that we are really in a POST request
    
    # Acces the form data:
    username = request.form["username"]
    password = request.form["password"]
    
    if username == "simon" and password == "safe":                                                                                                                                                             
        return "You are logged in Simon"                                                                                                                                                                                                       
    else:                                                                                                                                                                                                                                      
        error = "Invalid credentials"                                                                                                                                                                                                          
        return render_template("login.html", error=error) 

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/user')
def show_user_overview():
    users_str = "<br>".join(users.values())
    return '<h1>Our users</h1><br>{}'.format(users_str)

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'Welcome %s' % username   



if __name__=="__main__":
    app.run()