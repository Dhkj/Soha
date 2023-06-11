from db import db
from sqlalchemy.sql import text
from flask import session

#Refactor to use profile_id?
def set_session_profile(profile_name):
    session["profile_name"] = profile_name

def delete_session_profile():
    del session["profile_name"] #functions correctly?

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

def delete_profile(profile_name):
    #Add verification that the profile belongs to the user.
    try:
        sql = text("DELETE FROM profiles WHERE profile_name=:profile_name") #RETURNING COUNT DELETED??
        db.session.execute(sql, {"profile_name":profile_name})
        db.session.commit()
        #ADD FUNC TO VERIFY A DELETION WAS DONE -> IF NOT ERROR MSG
    except: #EVER EXCEPTS?
        return False
    
    #if session["profile_name"] == profile_name: # Not needed?
    #    del session["profile_name"]

    return True

def check_profile_exists(selected_profile):
    '''Checks that...'''
    # Could also be implemented using get_profiles(), or implementing an object variable containing all the profiles (and/or in a separate service module).
    try:
        user_id = session["user_id"]
    except:
        return False

    try:
        sql = text("SELECT user_id FROM profiles WHERE profile_name=:selected_profile")
        result = db.session.execute(sql, {"selected_profile":selected_profile})
        user_id_for_selected_profile = result.fetchone()[0]
    except:
        return False

    if user_id == user_id_for_selected_profile: # Test whether selecting another user's profile is possible.
        return True
    else:
        return False

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
