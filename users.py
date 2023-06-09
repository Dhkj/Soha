from db import db
from sqlalchemy.sql import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def register(username, password):
    if not input_validator(username, password):
        return False
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password, created) VALUES (:username, :password, NOW())")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    
    return login(username, password)

def logout():
    del session["user_id"]

def input_validator(username, password):
    return username_input_validator(username) and password_input_validator(password)

def username_input_validator(username):
    if len(username) < 8:
        return False
    
    return True

def password_input_validator(password):
    if len(password) < 5:
        return False
    
    return True
