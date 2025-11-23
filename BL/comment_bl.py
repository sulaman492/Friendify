from datetime import datetime

class Comment:
    def __init__(self, comment_id, user, text, timestamp=None):
        self.comment_id = comment_id
        self.user = user
        self.text = text  # MUST match FeedPage usage
        self.timestamp = timestamp or datetime.now()  # Use passed timestamp if exists

    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email
            },
            "text": self.text,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data):
        from BL.user_bl import User
        user_data = data["user"]
        user_obj = User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"]
        )
        timestamp = datetime.fromisoformat(data["timestamp"])
        return Comment(
            comment_id=data["comment_id"],
            user=user_obj,
            text=data["text"],
            timestamp=timestamp
        )
