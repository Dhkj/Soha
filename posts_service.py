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
        sql = text("SELECT Pr.profile_name, Po.content, Po.sent_at FROM posts Po, profiles Pr WHERE Po.profile_id=Pr.id ORDER BY Po.sent_at DESC") #DESCENDING? #MAX?
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
        #sql = text("SELECT id, profile_name, created FROM profiles WHERE user_id=:user_id")
        sql = text("SELECT Pr.profile_name, Po.content, Po.sent_at FROM posts Po, profiles Pr WHERE Po.profile_id=Pr.id AND Pr.profile_name=:profile_name ORDER BY Po.sent_at DESC") #DESCENDING?
        result = db.session.execute(sql, {"profile_name":profile_name})
        posts_by_session_profile = result.fetchall()
    except:
        return False

    return posts_by_session_profile
