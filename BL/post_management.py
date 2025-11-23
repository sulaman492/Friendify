from collections import deque
from BL.post_bl import Post
from BL.user_bl import User
from datetime import datetime
from BL.comment_bl import Comment
import os
import json

class PostManagement:
    def __init__(self):
        self.posts=deque()  
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "DL", "post.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.load_posts()

    def load_posts(self):
        if not os.path.exists(self.file_path):
            self.posts=deque()
            return
        try:
            with open(self.file_path,"r") as f:
                data=json.load(f)

                self.posts = deque([
    Post(
        post_id=p["post_id"],
        user=User(
            id=p["user"]["id"],
            username=p["user"]["username"],
            email=p["user"]["email"]
        ),
        content=p["content"],
        likes=p.get("likes", 0),
        comments=[Comment.from_dict(c) for c in p.get("comments", [])],
        timestamp=datetime.fromisoformat(p["timestamp"])
    )
    for p in data.get("posts", [])
])
            print("Loaded posts:", len(self.posts))
            for p in self.posts:
                print(p.post_id, p.content)
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
                    "email":post.user.email
                    },
                "content":post.content,
                "timestamp":post.timestamp.isoformat(),
                "likes":post.likes,
                "comments": [c.to_dict() for c in post.comments]
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
    
    def get_all_posts(self):
        return deque(sorted(self.posts,key = lambda p:p.timestamp,reverse=True))
    
    def search_post(self,keyword):
        keyword=keyword.lower().strip()
        if not keyword:
            return self.get_all_posts()

        results=[
            post for post in self.posts
            if keyword in post.content.lower() or keyword in post.user.username.lower()
        ]
        
        return deque(sorted(results,key=lambda p:p.timestamp,reverse=True))
    
    def like_post(self,post):
        post.likes+=1
        self.save_post()

    def find_post_by_post_id(self,post_id):
        for post in self.posts:
            if post_id==post.post_id:
                return post
        return None


    # def add_comment_to_post(self,post_id,comment):
    #     post=self.find_post_by_post_id(post_id)
    #     if post:
    #         post.add_comment(comment)
    #         self.save_post()

    def add_comment_to_post(self, post_id, user, text):
        post = self.find_post_by_post_id(post_id)
        if post:
            comment_id = len(post.comments) + 1
            comment = Comment(comment_id, user, text, timestamp=datetime.now())
            post.add_comment(comment)
            self.save_post()

    def sort_by_trending(self):

        def trending_post(post):
            return post.likes+post.comment_count
        return deque(sorted(self.posts,key=trending_post,reverse=True))