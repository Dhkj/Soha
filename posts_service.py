from db import db
from sqlalchemy.sql import text
from flask import session

def get_all_posts_and_likes():
    try:
        user_id = session["user_id"]
    except:
        return False
    
    sql = text("SELECT Po.id, Pr.profile_name, Po.content, Po.sent_at, COUNT(L.id) AS likes \
               FROM posts Po JOIN profiles Pr ON Po.profile_id=Pr.id \
               LEFT JOIN likes L ON L.post_id=Po.id \
               GROUP BY Po.id, Pr.profile_name, Po.content, Po.sent_at \
               ORDER BY Po.sent_at DESC")

    result = db.session.execute(sql)
    all_posts_and_likes = result.fetchall()

    return all_posts_and_likes

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
        sql = text("SELECT Po.id, Pr.profile_name, Po.content, Po.sent_at \
                   FROM posts Po, profiles Pr WHERE Po.profile_id=Pr.id \
                   AND Pr.profile_name=:profile_name ORDER BY Po.sent_at DESC")
        result = db.session.execute(sql, {"profile_name":profile_name})
        posts_by_session_profile = result.fetchall()
    except:
        return False

    return posts_by_session_profile

def get_post(post_id):
    try:
        user_id = session["user_id"]
    except:
        return False

    try:
        sql = text("SELECT Po.id, Pr.profile_name, Po.content, Po.sent_at \
                   FROM posts Po, profiles Pr WHERE Po.profile_id=Pr.id AND Po.id=:id")
        result = db.session.execute(sql, {"id":post_id})
        post = result.fetchone()
    except:
        return False

    return post

def get_comments(post_id):
    try:
        user_id = session["user_id"]
    except:
        return False

    try:
        sql = text("SELECT C.id, P.profile_name, C.content, C.sent_at \
                   FROM comments C, profiles P \
                   WHERE C.profile_id=P.id AND C.post_id=:post_id")
        result = db.session.execute(sql, {"post_id":post_id})
        all_comments_for_post = result.fetchall()
    except:
        return {}
    
    return all_comments_for_post

def delete_comment(deleted_comment_id):
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
        sql = text("DELETE FROM comments WHERE id=:comment_id AND profile_id=:profile_id")
        db.session.execute(sql, {"comment_id":deleted_comment_id, "profile_id":profile_id})
        db.session.commit()
    except:
        return False

    return True

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
        sql = text("INSERT INTO posts (content, profile_id, sent_at) \
                   VALUES (:content, :profile_id, NOW()) RETURNING id")
        result = db.session.execute(sql, {"content":post_content, "profile_id":profile_id})
        post_id = result.fetchone()[0]
        db.session.commit()
    except:
        return False

    return True

def add_new_comment(post_id, comment_content):
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
        sql = text("INSERT INTO comments (content, profile_id, post_id, sent_at) \
                   VALUES (:content, :profile_id, :post_id, NOW()) RETURNING id")
        result = db.session.execute(sql, {"content":comment_content, "profile_id":profile_id, "post_id":post_id})
        post_id = result.fetchone()[0]
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
        sql = text("DELETE FROM posts WHERE id=:post_id")
        db.session.execute(sql, {"post_id":deleted_post_id})
        db.session.commit()
    except:
        return False

    return True

def like_post(liked_post_id):
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
            db.session.commit()
            return True
        except:
            return False
        '''
    else:
        # Like:
        try:
            sql = text("INSERT INTO likes (profile_id, post_id, sent_at) \
                       VALUES (:profile_id, :post_id, NOW())")
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
