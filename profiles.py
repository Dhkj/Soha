from db import db
from sqlalchemy.sql import text
from flask import session

def set_session_profile(profile_name):
    session["profile_name"] = profile_name

def delete_session_profile():
    del session["profile_name"]

def add_profile(profile_name):
    try:
        user_id = session["user_id"]
    except:
        return False
    
    try:
        sql = text("INSERT INTO profiles (user_id, profile_name, created) \
                   VALUES (:user_id, :profile_name, NOW()) RETURNING id")
        result = db.session.execute(sql, {"user_id":user_id, "profile_name":profile_name})
        profile_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False

    try:
        sql = text("INSERT INTO profile_informations (profile_id, first_name, last_name, email,\
                    institution, city, country, motto, hobbies, status_text, profile_text)\
                    VALUES (:profile_id, :first_name, :last_name, :email,\
                    :institution, :city, :country, :motto, :hobbies, :status_text, :profile_text)")
        
        db.session.execute(sql, {"profile_id":profile_id, "first_name":"", "last_name":"", "email":"", \
                    "institution":"", "city":"", "country":"", "motto":"", "hobbies":"", "status_text":"", "profile_text":""})
        db.session.commit()
    except:
        return False
    
    return True

def delete_profile(profile_name):
    try:
        user_id = session["user_id"]
    except:
        return False
    
    try:
        sql = text("DELETE FROM profiles WHERE profile_name=:profile_name")
        db.session.execute(sql, {"profile_name":profile_name})
        db.session.commit()
    except:
        return False

    return True

def check_profile_exists(selected_profile):
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

    if user_id == user_id_for_selected_profile:
        return True
    else:
        return False

def get_profiles():
    try:
        user_id = session["user_id"]
    except:
        return False

    try:
        sql = text("SELECT id, profile_name, created FROM profiles WHERE user_id=:user_id")
        result = db.session.execute(sql, {"user_id":user_id})
        profiles = result.fetchall()
    except:
        return False

    return profiles

def get_profile_information_for_selected_profile():
    try:
        selected_profile_name = session["profile_name"]
    except:
        return False

    profile_id = find_profile_id_for_profile_name(selected_profile_name)

    try:
        
        sql = text("SELECT first_name, last_name, email, institution,\
                    city, country, motto, hobbies, status_text, profile_text\
                   FROM profile_informations WHERE profile_id=:profile_id")
        
        result = db.session.execute(sql, {"profile_id":profile_id})
        profile_information = result.fetchall()
    except:
        return False
    
    return profile_information

def update_profile(profile_information):
    try:
        user_id = session["user_id"]
    except:
        return False

    try:
        profile_name = session["profile_name"]
    except:
        return False

    profile_id = find_profile_id_for_profile_name(profile_name)

    #Implement using enumerator:
    first_name = profile_information[0]
    last_name = profile_information[1]
    email = profile_information[2]
    institution = profile_information[3]
    city = profile_information[4]
    country = profile_information[5]
    motto = profile_information[6]
    hobbies = profile_information[7]
    status_text = profile_information[8]
    profile_text = profile_information[9]

    if first_name != "":
        try:
            sql = text("UPDATE profile_informations SET first_name=:first_name WHERE profile_id=:profile_id")
            db.session.execute(sql, {"first_name":first_name, "profile_id":profile_id})
            db.session.commit()
        except:
            return False

    if last_name != "":
        try:
            sql = text("UPDATE profile_informations SET last_name=:last_name WHERE profile_id=:profile_id")
            db.session.execute(sql, {"last_name":last_name, "profile_id":profile_id})
            db.session.commit()
        except:
            return False

    if email != "":
        try:
            sql = text("UPDATE profile_informations SET email=:email WHERE profile_id=:profile_id")
            db.session.execute(sql, {"email":email, "profile_id":profile_id})
            db.session.commit()
        except:
            return False
        
    if institution != "":
        try:
            sql = text("UPDATE profile_informations SET institution=:institution WHERE profile_id=:profile_id")
            db.session.execute(sql, {"institution":institution, "profile_id":profile_id})
            db.session.commit()
        except:
            return False
        
    if city != "":
        try:
            sql = text("UPDATE profile_informations SET city=:city WHERE profile_id=:profile_id")
            db.session.execute(sql, {"city":city, "profile_id":profile_id})
            db.session.commit()
        except:
            return False

    if country != "":
        try:
            sql = text("UPDATE profile_informations SET country=:country WHERE profile_id=:profile_id")
            db.session.execute(sql, {"country":country, "profile_id":profile_id})
            db.session.commit()
        except:
            return False

    if motto != "":
        try:
            sql = text("UPDATE profile_informations SET motto=:motto WHERE profile_id=:profile_id")
            db.session.execute(sql, {"motto":motto, "profile_id":profile_id})
            db.session.commit()
        except:
            return False
        
    if hobbies != "":
        try:
            sql = text("UPDATE profile_informations SET hobbies=:hobbies WHERE profile_id=:profile_id")
            db.session.execute(sql, {"hobbies":hobbies, "profile_id":profile_id})
            db.session.commit()
        except:
            return False
        
    if status_text != "":
        try:
            sql = text("UPDATE profile_informations SET status_text=:status_text WHERE profile_id=:profile_id")
            db.session.execute(sql, {"status_text":status_text, "profile_id":profile_id})
            db.session.commit()
        except:
            return False
        
    if profile_text != "":
        try:
            sql = text("UPDATE profile_informations SET profile_text=:profile_text WHERE profile_id=:profile_id")
            db.session.execute(sql, {"profile_text":profile_text, "profile_id":profile_id})
            db.session.commit()
        except:
            return False

    return True

def find_profile_id_for_profile_name(profile_name):
    try:
        sql = text("SELECT id FROM profiles WHERE profile_name=:profile_name")
        result = db.session.execute(sql, {"profile_name":profile_name})
        id_for_profile_name = result.fetchone()[0]
    except:
        return False
    
    return id_for_profile_name
