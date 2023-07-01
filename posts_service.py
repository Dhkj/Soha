from db import db
from sqlalchemy.sql import text
from flask import session

#Todo: add functinality to get posts in batches of certain size.

#No longer in use.
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

def get_all_posts_and_likes():
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
    
    sql = text("SELECT Po.id, Pr.profile_name, Po.content, Po.sent_at, COUNT(L.id) AS likes \
               FROM posts Po JOIN profiles Pr ON Po.profile_id=Pr.id \
               LEFT JOIN likes L ON L.post_id=Po.id \
               GROUP BY Po.id, Pr.profile_name, Po.content, Po.sent_at \
               ORDER BY Po.sent_at DESC") #DESCENDING? #MAX?
    
    result = db.session.execute(sql)
    all_posts_and_likes = result.fetchall()

    return all_posts_and_likes

#test to check multiple likes from different profiles

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
        sql = text("INSERT INTO posts (content, profile_id, sent_at) VALUES (:content, :profile_id, NOW()) RETURNING id")
        result = db.session.execute(sql, {"content":post_content, "profile_id":profile_id})
        post_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False


    #NO LONGER!!
    #Has to be added an empty row in table likes for listing to work in /posts.
    #Only the post creator profile has 'False' like in table likes for the post in the beginning.
    '''
    try:
        sql = text("INSERT INTO likes (profile_id, post_id, sent_at) VALUES (:profile_id, :post_id, NOW())")
        db.session.execute(sql, {"profile_id":profile_id, "post_id":post_id})
        db.session.commit()
    except:
        return False
    '''

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



#refactor likes?
#def get_likes():

def like_post(liked_post_id):
    #Add checks for the session user and profile?

    try:
        profile_name = session["profile_name"]
    except:
        return False

    profile_id = find_profile_id_for_profile_name(profile_name)

    like_id = 0

    try:
        # Checks whether already liked:
        sql = text("SELECT id FROM likes WHERE profile_id=:profile_id AND post_id=:post_id")
        result = db.session.execute(sql, {"profile_id":profile_id, "post_id":liked_post_id})
        like_id = result.fetchone()[0]
    except:
        pass

    if like_id:
        # Already liked: cannot like again.
        return True
    
        '''
        #Unlike: for further implementation
        try:
            sql = text("DELETE FROM likes WHERE id=:id")
            db.session.execute(sql, {"id":like_id})
                                # Value 0 if no row?
            db.session.commit()
            return True
        except:
            return False
        '''
    else:
        # Like:
        try:
            sql = text("INSERT INTO likes (profile_id, post_id, sent_at) VALUES (:profile_id, :post_id, NOW())") #TRUE?
            db.session.execute(sql, {"profile_id":profile_id, "post_id":liked_post_id})
            db.session.commit()
            return True
        except:
            return False

def unlike_post(unliked_post_id):
    try:
        profile_name = session["profile_name"]
    except:
        return False

    profile_id = find_profile_id_for_profile_name(profile_name)

    unlike_id = 0

    try:
        # Checks whether already liked:
        sql = text("SELECT id FROM likes WHERE profile_id=:profile_id AND post_id=:post_id")
        result = db.session.execute(sql, {"profile_id":profile_id, "post_id":unliked_post_id})
        unlike_id = result.fetchone()[0]
    except:
        pass

    if unlike_id:
        # Unlike:
        try:
            sql = text("DELETE FROM likes WHERE id=:id")
            db.session.execute(sql, {"id":unlike_id})
            db.session.commit()
            return True
        except:
            return False
    else:
        # Not liked yet: cannot unlike.
        return True



    #NO LONGER IN USE:
    # Checks whether already liked:
    '''
    try:
        sql = text("SELECT COUNT(*) FROM likes WHERE profile_id=:profile_id AND post_id=:post_id")
        result = db.session.execute(sql, {"profile_id":profile_id, "post_id":liked_post_id})
        # Value 0 if no row?
        amount_of_likes_for_the_post_by_profile = result.fetchone()[0]
    except:
        amount_of_likes_for_the_post_by_profile = 0

    if amount_of_likes_for_the_post_by_profile:
        try:
            sql = text("UPDATE likes SET likes=TRUE WHERE profile_id=:profile_id AND post_id=:post_id")
            db.session.execute(sql, {"profile_id":profile_id, "post_id":liked_post_id})
            db.session.commit()
        except:
            False
    else:
        try:
            sql = text("INSERT INTO likes (profile_id, post_id, likes, sent_at) VALUES (:profile_id, :post_id, TRUE, NOW())") #TRUE?
            db.session.execute(sql, {"profile_id":profile_id, "post_id":liked_post_id})
            db.session.commit()
        except:
            return False
    '''
    #return True
