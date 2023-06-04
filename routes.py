from app import app
from flask import render_template, request, redirect
#import messages, users
import users

@app.route("/")
#@app.route("/profile")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message='We are sorry! The given two passwords do not match. Please return to the previous page and try again!')
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message='We are sorry! The registration was unsuccessful. Please return to the previous page and try again!')

#@app.route("/login", methods=["GET", "POST"]) -> GET redirects to Front Page?
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
        #return redirect("/profile")?
    else:
        return render_template("error.html", message='We are sorry! The login was unsuccessful. Please return to the previous page and try again!')

    '''
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Error msg")
    '''

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

@app.route("/profiles")
def profiles():
    return render_template("profiles.html")

@app.route("/friends")
def friends():
    return render_template("friends.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/posts")
def posts():
    return render_template("posts.html")



'''
@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", count=len(list), messages=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    if messages.send(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
'''
