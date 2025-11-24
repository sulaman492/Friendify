from BL.post_bl import Post
from BL.user_bl import User
from datetime import datetime
from BL.comment_bl import Comment
from DataStructures.Stack import Stack
from DataStructures.Queue import Queue
import os
import json

class PostManagement:
    def __init__(self):
        self.posts = Queue()  # Use custom Queue
        self.deleted_posts = Stack(max_size=10)  # Use custom Stack
        self.like_history = Stack()
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "DL", "post.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.load_posts()

    def load_posts(self):
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                for p in data.get("posts", []):
                    post = Post(
                        post_id=p["post_id"],
                        user=User(
                            id=p["user"]["id"],
                            username=p["user"]["username"],
                            email=p["user"]["email"]
                        ),
                        content=p["content"],
                        comments=[Comment.from_dict(c) for c in p.get("comments", [])],
                        timestamp=datetime.fromisoformat(p["timestamp"])
                    )
                    # Set liked_users AFTER creating the Post
                    post.liked_users = set(p.get("liked_users", []))

                    self.posts.enqueue(post)
        except:
            self.posts = Queue()

    def save_post(self):
        with open(self.file_path, "w") as f:
            data = {"posts": [
                {
                    "post_id": post.post_id,
                    "user": {
                        "id": post.user.id,
                        "username": post.user.username,
                        "email": post.user.email
                    },
                    "content": post.content,
                    "timestamp": post.timestamp.isoformat(),
                    "comments": [c.to_dict() for c in post.comments],
                    "liked_users": list(post.liked_users)
                } for post in self.posts.items  # Access internal list
            ]}
            json.dump(data, f, indent=4)

    def create_post(self, user, content):
        if not content or content.strip() == "":
            raise ValueError("Post cannot be empty")
        post_id = max([p.post_id for p in self.posts.items], default=0) + 1
        post = Post(post_id, user, content)
        self.posts.enqueue(post)
        self.save_post()
        return post

    def edit_post(self, post_id, new_content):
        for post in self.posts.items:
            if post.post_id == post_id:
                post.content = new_content
                self.save_post()
                return True
        return False

    def delete_post(self, post_id):
        for post in self.posts.items:
            if post.post_id == post_id:
                self.posts.items.remove(post)  # remove from queue
                if not self.deleted_posts.is_full():
                    self.deleted_posts.push(post)
                self.save_post()
                return True
        return False

    def undo_post(self):
        if self.deleted_posts.is_empty():
            return False
        post = self.deleted_posts.pop()
        self.posts.enqueue(post)
        self.save_post()
        return True

    def get_all_posts(self):
        return sorted(self.posts.items, key=lambda p: p.timestamp, reverse=True)

    def search_post(self, keyword):
       keyword = keyword.lower().strip()
       if not keyword:
           return self.get_all_posts()
       results = [post for post in self.posts.items
                  if keyword in post.content.lower() or keyword in post.user.username.lower()]
       return sorted(results, key=lambda p: p.timestamp, reverse=True)

    def toggle_like_post(self, post, user):
        if not hasattr(post, "liked_users"):
            post.liked_users = set()

        if user.username in post.liked_users:
            # User is unliking
            post.liked_users.remove(user.username)
            post.likes -= 1
            # Remove from like_history if exists
            temp_stack = Stack()
            while not self.like_history.is_empty():
                p, u = self.like_history.pop()
                if p != post or u != user:
                    temp_stack.push((p, u))
            while not temp_stack.is_empty():
                self.like_history.push(temp_stack.pop())
            self.save_post()
            return "disliked"
        else:
            # User is liking
            post.liked_users.add(user.username)
            post.likes += 1
            self.like_history.push((post, user))
            self.save_post()
            return "liked"

    # Undo the most recent like
    def undo_like(self):
        if self.like_history.is_empty():
            return None
        post, user = self.like_history.pop()
        if user.username in post.liked_users:
            post.liked_users.remove(user.username)
            post.likes -= 1
            self.save_post()
            return post
        return None


    def find_post_by_post_id(self, post_id):
        for post in self.posts.items:
            if post.post_id == post_id:
                return post
        return None

    def add_comment_to_post(self, post_id, user, text):
        post = self.find_post_by_post_id(post_id)
        if post:
            comment_id = len(post.comments) + 1
            comment = Comment(comment_id, user, text, timestamp=datetime.now())
            post.add_comment(comment)
            self.save_post()

    def sort_by_trending(self):
        return sorted(self.posts.items, key=lambda post: post.likes + post.comment_count, reverse=True)
