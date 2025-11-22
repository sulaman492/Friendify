from collections import deque
from BL.post_bl import Post
from datetime import datetime
import os
import json

class PostManagement:
    def __init__(self):
        self.posts=deque()  
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "DL", "post.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self._load_posts()

    def load_posts(self):
        if not os.path.exists(self.file_path):
            self.posts=deque()
            return
        try:
            with open(self.file_path,"r") as f:
                data=json.load(f)

                self.posts=deque([
                     Post(
                          post_id=p["post_id"],
                          user=p["user"],
                          content=p["content"]
                     ) for p in data.get("posts",[])
                ])

        except:
                self.posts=deque()
                return

    def save_post(self):
        with open(self.file_path,"w") as f:
            data={"posts":[{
                "post_id":post.post_id,
                "user":{
                    "id":post.user.id,
                    "username":post.user.username,
                    "email":post.user.username
                    },
                "content":post.content,
                "timestamp":post.timestamp.isoformat()
            }for post in self.posts
            ]}
            json.dump(data,f,indent=4)

    def create_post(self,user,content):
        if not content or content.strip()=="":
            raise ValueError("Post cannot be empty")
    
        post_id=max([p.post_id for p in self.posts],default=0)+1
        post=Post(post_id,user,content)
        self.posts.append(post)
        self.save_post()
        return post

    def edit_post(self,post_id,new_content):
        self.load_posts()
        for post in self.posts:
            if post.post_id==post_id:
                post.content=new_content
                self.save_post()
                return True
        return False

    def delete_post(self,post_id):
        self.load_posts()
        for post in self.posts:
            if post.post_id==post_id:
                self.posts.remove(post)
                self.save_post()
                return True
        return False