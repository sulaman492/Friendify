import json
import os
from datetime import datetime 
class Post:
    def __init__(self,post_id,user,content):
          
        self.post_id=post_id
        self.user=user
        self.content=content
        self.timestamp=datetime.now()
        self.likes = 0

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] User {self.user.username}: {self.content}"
