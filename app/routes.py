# app/routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from .schemas import UserCreate, UserRead, UserUpdate, PostCreate, PostRead
from . import controllers

router = APIRouter(prefix="/api", tags=["api"])

# Users
@router.post("/users", response_model=UserRead)
def api_create_user(u: UserCreate):
    existing = controllers.get_user_by_username(u.username)
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")
    user = controllers.create_user(u)
    return UserRead(
        uid=user.uid,
        username=user.username,
        full_name=user.full_name,
        bio=user.bio,
        created_at=user.created_at
    )

@router.get("/users/{uid}", response_model=UserRead)
def api_get_user(uid: str):
    user = controllers.get_user_by_uid(uid)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return UserRead(
        uid=user.uid,
        username=user.username,
        full_name=user.full_name,
        bio=user.bio,
        created_at=user.created_at
    )

@router.patch("/users/{uid}", response_model=UserRead)
def api_update_user(uid: str, u: UserUpdate):
    updated = controllers.update_user(uid, u)
    if not updated:
        raise HTTPException(status_code=404, detail="user not found")
    return UserRead(
        uid=updated.uid,
        username=updated.username,
        full_name=updated.full_name,
        bio=updated.bio,
        created_at=updated.created_at
    )

@router.delete("/users/{uid}")
def api_delete_user(uid: str):
    ok = controllers.delete_user(uid)
    if not ok:
        raise HTTPException(status_code=404, detail="user not found")
    return {"ok": True}

@router.post("/users/{follower_uid}/follow/{followee_uid}")
def api_follow(follower_uid: str, followee_uid: str):
    if controllers.follow_user(follower_uid, followee_uid):
        return {"ok": True}
    raise HTTPException(status_code=400, detail="unable to follow")

@router.post("/users/{follower_uid}/unfollow/{followee_uid}")
def api_unfollow(follower_uid: str, followee_uid: str):
    if controllers.unfollow_user(follower_uid, followee_uid):
        return {"ok": True}
    raise HTTPException(status_code=400, detail="unable to unfollow")

# Posts
@router.post("/posts", response_model=PostRead)
def api_create_post(p: PostCreate):
    post = controllers.create_post(p)
    if not post:
        raise HTTPException(status_code=404, detail="author not found")
    # get author uid
    # author relationship: post.author.single() is possible if single author
    author_rel = next(iter(post.author.all()), None)
    author_uid = author_rel.uid if author_rel else None
    return PostRead(
        uid=post.uid,
        content=post.content,
        media=post.media or {},
        created_at=post.created_at,
        author_uid=author_uid
    )

@router.get("/posts/{uid}", response_model=PostRead)
def api_get_post(uid: str):
    p = controllers.get_post(uid)
    if not p:
        raise HTTPException(status_code=404, detail="post not found")
    author = next(iter(p.author.all()), None)
    author_uid = author.uid if author else None
    return PostRead(
        uid=p.uid,
        content=p.content,
        media=p.media or {},
        created_at=p.created_at,
        author_uid=author_uid
    )

@router.get("/posts", response_model=List[PostRead])
def api_list_posts(limit: int = 20):
    posts = controllers.list_posts(limit)
    out = []
    for p in posts:
        author = next(iter(p.author.all()), None)
        author_uid = author.uid if author else None
        out.append(PostRead(
            uid=p.uid, content=p.content, media=p.media or {}, created_at=p.created_at, author_uid=author_uid
        ))
    return out

@router.patch("/posts/{uid}", response_model=PostRead)
def api_update_post(uid: str, body: dict):
    p = controllers.update_post(uid, content=body.get("content"), media=body.get("media"))
    if not p:
        raise HTTPException(status_code=404, detail="post not found")
    author = next(iter(p.author.all()), None)
    author_uid = author.uid if author else None
    return PostRead(uid=p.uid, content=p.content, media=p.media or {}, created_at=p.created_at, author_uid=author_uid)

@router.delete("/posts/{uid}")
def api_delete_post(uid: str):
    ok = controllers.delete_post(uid)
    if not ok:
        raise HTTPException(status_code=404, detail="post not found")
    return {"ok": True}