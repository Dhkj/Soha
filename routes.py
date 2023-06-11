from app import app
from flask import render_template, request, redirect
#import messages, users
import users, profiles

@app.route("/")
#@app.route("/profile")
def index():
    #profiles.get_profiles()
    return render_template("index.html")

@app.route("/profiles", methods=["GET", "POST"])
#@app.route("/profiles/<int:profile_id>", methods=["GET", "POST"])
def profiles_page():
    if request.method == "GET":
        return render_template("profiles.html", profiles=profiles.get_profiles()) #profiles here ok? no confusion?
    if request.method == "POST":
        if request.form["form_type"] == "selected_profile":
            selected_profile = request.form["selected_profile"]

            if len(selected_profile) == 0:
                return render_template("error.html", message="No profile selected!")

            # No longer needed if profiles.html changed to use select?:
            if profiles.check_profile_exists(selected_profile):
                profiles.set_session_profile(selected_profile) #Change to use profile_id?            
                return redirect("/profiles")
            else:
                return render_template("error.html", message="We are sorry! You do not have a profile with the selected profile name!")
        
        elif request.form["form_type"] == "profile_name":
            profile_name = request.form["profile_name"]
            if len(profile_name) < 2:
                return render_template("error.html", message="Profile name is too short! Please give a profile name of at least two characters in length!")
            if profiles.add_profile(profile_name):
                return redirect("/profiles")
            else:
                return render_template("error.html", message="Given profile name already exists!") #"Error message // you have not logged in? / profilename already taken??")

        elif request.form["form_type"] == "change_profile":
            profiles.delete_session_profile()
            return redirect("/profiles")
        
        elif request.form["form_type"] == "delete_profile":
            profile_name_to_be_deleted = request.form["delete_profile"]
            # Add checks whether deleted profile name belongs/exists for the user and whether deletion was successfull? -> error msg?
            profiles.delete_profile(profile_name_to_be_deleted)
            return redirect("/profiles")

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

'''
@app.route("/profiles")
#def profiles():
def profiles_page():
    return render_template("profiles.html")
'''
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
