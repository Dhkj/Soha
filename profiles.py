from db import db
from sqlalchemy.sql import text
from flask import session

#Refactor to use profile_id?
def set_session_profile(profile_name):
    session["profile_name"] = profile_name

def delete_session_profile():
    del session["profile_name"] #toimii?

#add delete_profile()

def add_profile(profile_name):
    try:
        user_id = session["user_id"]
    except:
        return False
    
    try:
        sql = text("INSERT INTO profiles (user_id, profile_name, created) VALUES (:user_id, :profile_name, NOW())")
        db.session.execute(sql, {"user_id":user_id, "profile_name":profile_name})
        db.session.commit()
    except:
        return False
    
    return True

def get_profiles():
    try:
        user_id = session["user_id"]
    except:
        return False

    sql = text("SELECT id, profile_name, created FROM profiles WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    profiles = result.fetchall()

    # Everything works if no profiles?

    return profiles
