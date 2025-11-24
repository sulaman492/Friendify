import json
import os
from datetime import datetime 
class Post:
    def __init__(self, post_id, user, content, likes=0, comments=None, timestamp=None):
        self.post_id = post_id
        self.user = user
        self.content = content
        self.likes = likes
        self.comments = comments or []  # must be Comment objects
        self.timestamp = timestamp or datetime.now()
        self.liked_users = set()

    def add_comment(self, comment):
        self.comments.append(comment)
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] User {self.user.username}: {self.content}"
    
    @property
    def comment_count(self):
        return len(self.comments)
    