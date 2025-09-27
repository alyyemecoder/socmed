# app/models.py
from neomodel import (
    StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty,
    DateTimeProperty, RelationshipTo, RelationshipFrom, JSONProperty
)
from datetime import datetime

class User(StructuredNode):
    uid = UniqueIdProperty()                # unique id
    username = StringProperty(unique_index=True, required=True)
    full_name = StringProperty()
    bio = StringProperty(default="")
    created_at = DateTimeProperty(default_now=True)

    posts = RelationshipTo('Post', 'POSTED')
    follows = RelationshipTo('User', 'FOLLOWS')
    followers = RelationshipFrom('User', 'FOLLOWS')


class Post(StructuredNode):
    uid = UniqueIdProperty()
    content = StringProperty(required=True)
    media = JSONProperty()  # store media metadata if needed
    created_at = DateTimeProperty(default_now=True)

    author = RelationshipFrom('User', 'POSTED')
