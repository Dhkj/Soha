from db import db
from sqlalchemy.sql import text
from flask import session

#Todo: add functinality to get posts in batches of certain size.

def get_all_posts():
    try:
        user_id = session["user_id"]
    except:
        return False
    '''
    try:
        profile_name = session["profile_name"]
    except:
        return False
    '''
    try:
        sql = text("SELECT Po.id, Pr.profile_name, Po.content, Po.sent_at FROM posts Po, profiles Pr WHERE Po.profile_id=Pr.id ORDER BY Po.sent_at DESC") #DESCENDING? #MAX?
        result = db.session.execute(sql) #ok? #, {"profile_name":profile_name})
        all_posts = result.fetchall()
    except:
        return False

    return all_posts

def get_posts_by_session_profile():
    try:
        user_id = session["user_id"]
    except:
        return False
    
    try:
        profile_name = session["profile_name"]
    except:
        return False

    try:
        sql = text("SELECT Po.id, Pr.profile_name, Po.content, Po.sent_at FROM posts Po, profiles Pr WHERE Po.profile_id=Pr.id AND Pr.profile_name=:profile_name ORDER BY Po.sent_at DESC") #DESCENDING?
        result = db.session.execute(sql, {"profile_name":profile_name})
        posts_by_session_profile = result.fetchall()
    except:
        return False

    return posts_by_session_profile

def add_new_post(post_content):
    try:
        user_id = session["user_id"]
    except:
        return False
    
    try:
        profile_name = session["profile_name"]
    except:
        return False
    
    profile_id = find_profile_id_for_profile_name(profile_name)

    try:
        sql = text("INSERT INTO posts (content, profile_id, sent_at) VALUES (:content, :profile_id, NOW())")
        db.session.execute(sql, {"content":post_content, "profile_id":profile_id})
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

def delete_post(deleted_post_id):
    try:
        sql = text("DELETE FROM posts WHERE id=:post_id") #RETURNING COUNT DELETED??
        db.session.execute(sql, {"post_id":deleted_post_id})
        db.session.commit()
        #ADD FUNC TO VERIFY A DELETION WAS DONE -> IF NOT ERROR MSG
    except: #EVER EXCEPTS?
        return False
    
    #if session["profile_name"] == profile_name: # Not needed?
    #    del session["profile_name"]

    return True
