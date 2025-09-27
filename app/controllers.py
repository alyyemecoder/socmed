# app/controllers.py
from typing import List, Optional
from neomodel import DoesNotExist
from .models import User, Post
from .schemas import UserCreate, UserUpdate, PostCreate
from datetime import datetime

# ----- User CRUD -----
def create_user(data: UserCreate) -> User:
    user = User(username=data.username, full_name=data.full_name or "", bio=data.bio or "")
    user.save()
    return user

def get_user_by_uid(uid: str) -> Optional[User]:
    try:
        return User.nodes.get(uid=uid)
    except DoesNotExist:
        return None

def get_user_by_username(username: str) -> Optional[User]:
    try:
        return User.nodes.get(username=username)
    except DoesNotExist:
        return None

def update_user(uid: str, data: UserUpdate) -> Optional[User]:
    u = get_user_by_uid(uid)
    if not u:
        return None
    if data.full_name is not None:
        u.full_name = data.full_name
    if data.bio is not None:
        u.bio = data.bio
    u.save()
    return u

def delete_user(uid: str) -> bool:
    u = get_user_by_uid(uid)
    if not u:
        return False
    u.delete()
    return True

def follow_user(follower_uid: str, followee_uid: str) -> bool:
    follower = get_user_by_uid(follower_uid)
    followee = get_user_by_uid(followee_uid)
    if not follower or not followee or follower.uid == followee.uid:
        return False
    follower.follows.connect(followee)
    return True

def unfollow_user(follower_uid: str, followee_uid: str) -> bool:
    follower = get_user_by_uid(follower_uid)
    followee = get_user_by_uid(followee_uid)
    if not follower or not followee:
        return False
    try:
        follower.follows.disconnect(followee)
    except Exception:
        pass
    return True

# ----- Post CRUD -----
def create_post(data: PostCreate) -> Optional[Post]:
    try:
        author = User.nodes.get(uid=data.author_uid)
    except DoesNotExist:
        return None
    post = Post(content=data.content, media=data.media or {})
    post.save()
    # create relationship
    author.posts.connect(post)
    return post

def get_post(uid: str) -> Optional[Post]:
    try:
        return Post.nodes.get(uid=uid)
    except DoesNotExist:
        return None

def list_posts(limit: int = 20) -> List[Post]:
    return list(Post.nodes.order_by('-created_at')[:limit])

def update_post(uid: str, content: Optional[str]=None, media: Optional[dict]=None) -> Optional[Post]:
    p = get_post(uid)
    if not p:
        return None
    if content is not None:
        p.content = content
    if media is not None:
        p.media = media
    p.save()
    return p

def delete_post(uid: str) -> bool:
    p = get_post(uid)
    if not p:
        return False
    p.delete()
    return True
