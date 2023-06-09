from app import app
from flask import render_template, request, redirect, session, abort
import users, profiles, posts_service

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profiles", methods=["GET", "POST"])
def profiles_page():
    if request.method == "GET":
        return render_template("profiles.html", profiles=profiles.get_profiles(), \
                               profile_information=profiles.get_profile_information_for_selected_profile())
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
        if request.form["form_type"] == "selected_profile":
            selected_profile = request.form["selected_profile"]
            if len(selected_profile) == 0:
                return render_template("error.html", message="No profile selected!")
            if profiles.check_profile_exists(selected_profile):
                profiles.set_session_profile(selected_profile)          
                return redirect("/profiles")
            else:
                return render_template("error.html", message="We are sorry! \
                                       You do not have a profile with the selected profile name!")        
        elif request.form["form_type"] == "profile_name":
            profile_name = request.form["profile_name"]
            if len(profile_name) < 2:
                return render_template("error.html", message="Profile name is too short! \
                                       Please give a profile name of at least two characters in length!")
            if profiles.add_profile(profile_name):
                return redirect("/profiles")
            else:
                return render_template("error.html", message="Given profile name already exists!")
        elif request.form["form_type"] == "change_profile":
            profiles.delete_session_profile()
            return redirect("/profiles")        
        elif request.form["form_type"] == "delete_profile":
            profile_name_to_be_deleted = request.form["delete_profile"]
            profiles.delete_profile(profile_name_to_be_deleted)
            return redirect("/profiles")

@app.route("/profile_update", methods=["GET", "POST"])
def profile_update():
    if request.method == "GET":
        return render_template("profile_update.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        institution = request.form["institution"]
        city = request.form["city"]
        country = request.form["country"]
        motto = request.form["motto"]
        hobbies = request.form["hobbies"]
        status_text = request.form["status_text"]
        profile_text = request.form["profile_text"]

        profile_information = [first_name,
                               last_name,
                               email,
                               institution,
                               city,
                               country,
                               motto,
                               hobbies,
                               status_text,
                               profile_text]

        profiles.update_profile(profile_information)
        return redirect("/profiles")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 5:
            return render_template("error.html", \
                                   message="We are sorry! The given username was too short. \
                                    Please return to the previous page and choose a username at least 5 charaters in length!")
        elif len(username) > 30:
            return render_template("error.html", \
                                   message="We are sorry! The given username was too long. \
                                    Please return to the previous page and choose a username no more than 30 charaters in length!")
        password1 = request.form["password1"]
        if len(password1) < 5:
            return render_template("error.html", \
                                   message="We are sorry! The chosen password was too short. \
                                    Please return to the previous page and choose a password at least 5 charaters in length!")
        elif len(password1) > 30:
            return render_template("error.html", \
                                   message="We are sorry! The given password was too long. \
                                    Please return to the previous page and choose a password no more than 30 charaters in length!")
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="We are sorry! The given two passwords do not match. \
                                   Please return to the previous page and try again!")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="We are sorry! The registration was unsuccessful. \
                                   Please return to the previous page and try again!")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    if len(username) == 0:
        return render_template("error.html", message='We are sorry! \
                               No username was entered. Please return to the previous page and try again!')
    password = request.form["password"]
    if len(password) == 0:
        return render_template("error.html", message='We are sorry! \
                               No password was entered. Please return to the previous page and try again!')
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message='We are sorry! \
                               The given username and password do not match. Please return to the previous page and try again!')

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

@app.route("/friends")
def friends():
    return render_template("friends.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/posts", methods=["GET", "POST"])
def posts():
    if request.method == "GET":
        all_posts_and_likes = posts_service.get_all_posts_and_likes()
        number_of_posts = len(all_posts_and_likes)
        return render_template("posts.html", number_of_posts=number_of_posts, \
                               all_posts_and_likes=all_posts_and_likes)
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)        
        if request.form["post_type"] == "delete_post":
            deleted_post_id = request.form["deleted_post_id"]
            if posts_service.delete_post(deleted_post_id):
                return redirect("/posts")
            else:
                return render_template("error.html", message='We are sorry! \
                                       The deletion was unsuccessful. Please return to the previous page and try again!')
        elif request.form["post_type"] == "like":
            liked_post_id = request.form["liked_post_id"]
            if posts_service.like_post(liked_post_id):
                return redirect("/posts")
            else:
                return render_template("error.html", message='We are sorry! \
                                       There was an unexpected error. Please return to the previous page and try again!')
        elif request.form["post_type"] == "unlike":
            unliked_post_id = request.form["unliked_post_id"]
            if posts_service.unlike_post(unliked_post_id):
                return redirect("/posts")
            else:
                return render_template("error.html", message='We are sorry! \
                                       There was an unexpected error. Please return to the previous page and try again!')
        elif request.form["post_type"] == "new_post":
            post_content = request.form["new_post_content"]
            if post_content == "":
                return render_template("error.html", message='We are sorry! \
                                       Your new post was empty! Please return to the previous page and try again!')            
            if len(post_content) > 100:
                return render_template("error.html", message='We are sorry! \
                                       Your new post was more than 100 characters in length! Please return to the previous page and try again!')
            elif posts_service.add_new_post(post_content):
                return redirect("/posts")
            else:
                return render_template("error.html", message='We are sorry! \
                                       Unfortunately adding your new post was unsuccessful. Please return to the previous page and try again!')

@app.route("/comments/<int:post_id>", methods=["GET", "POST"])
def comments(post_id):
    if request.method == "GET":
        post = posts_service.get_post(post_id)

        if not post:
            return render_template("error.html", message='We are sorry! \
                                   No such post exists. Please return to the previous page and try again!')

        comments = posts_service.get_comments(post_id) #Add
        number_of_comments = len(comments)
        return render_template("comments.html", post_id=post_id, post=post, \
                               comments=comments, number_of_comments=number_of_comments)
    if request.method == "POST":
        post_id = request.form["post_id"]      
        address = "/comments/" + post_id

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)        
        if request.form["post_type"] == "delete_comment":
            deleted_comment_id = request.form["deleted_comment_id"]

            if posts_service.delete_comment(deleted_comment_id):
                return redirect(address)
            else:
                return render_template("error.html", message='We are sorry! \
                                       The deletion was unsuccessful. Please return to the previous page and try again!')     
        elif request.form["post_type"] == "new_comment":
            comment_content = request.form["new_comment_content"]

            if comment_content == "":
                return render_template("error.html", message='We are sorry! \
                                       Your new comment was empty! Please return to the previous page and try again!')
            elif posts_service.add_new_comment(post_id, comment_content):
                return redirect(address)           
            else:
                return render_template("error.html", message='We are sorry! \
                                       Unfortunately adding your new post was unsuccessful. Please return to the previous page and try again!')
