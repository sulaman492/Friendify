import os
import json
from .friend_bl import Friend  # your Friend class

class FriendManager:
    def __init__(self):
        # Path to friendships JSON
        base = os.path.dirname(os.path.dirname(__file__))
        self.file_path = os.path.join(base, "DL", "friends.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # Ensure file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({"friendships": []}, f, indent=4)

    # ---------------------------
    # Load friends
    # ---------------------------
    def load_friend(self, user_id):
        f = Friend(0, 0)  # dummy object just to reuse functions
        return f.load_friend(user_id)

    # ---------------------------
    # Send Request
    # ---------------------------
    def send_request(self, sender_id, receiver_id):
        f = Friend(sender_id, receiver_id)
        return f.send_request(sender_id, receiver_id)

    # ---------------------------
    # Accept request
    # ---------------------------
    def accept_friend_request(self, sender_id, receiver_id):
        f = Friend(sender_id, receiver_id)
        return f.accept_freind_request(sender_id, receiver_id)

    # ---------------------------
    # View pending
    # ---------------------------
    def view_pending_requests(self, user_id):
        f = Friend(0, 0)
        return f.view_pending_requests(user_id)

    def get_all_relationships(self, user_id):
        """
        Returns all user IDs that have any relationship with current user
        (pending, accepted, or rejected).
        """
        f = Friend(0, 0)
        return f.get_all_relationships(user_id)