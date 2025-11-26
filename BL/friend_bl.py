import os
import json
class FriendNode:
    def __init__(self,friend_id,friend_name):
        self.friend_id=friend_id
        self.friend_name=friend_name
        self.next=None

class FriendLinkedList:
    
    def __init__(self):
        self.head=None

    def add_friend(self,friend_id,friend_name):
        new_node=FriendNode(friend_id,friend_name)
        if not self.head:
            self.head=new_node
        
        else:
            temp=self.head
            while temp.next:
                temp=temp.next
            temp.next=new_node
    
    def sort_friends(self):
        # If list is empty or has only one friend — nothing to sort
        if not self.head or not self.head.next:
            return
    
        # Step 1: Extract nodes into a list
        nodes = []
        temp = self.head
        while temp:
            nodes.append(temp)
            temp = temp.next
    
        # Step 2: Sort nodes by friend_name A → Z
        nodes.sort(key=lambda x: x.friend_name.lower())
    
        # Step 3: Rebuild linked list
        self.head = nodes[0]
        temp = self.head
        for node in nodes[1:]:
            temp.next = node
            temp = node
    
        temp.next = None    

class Friend:
    def __init__(self,user_id1,user_id2,status="pending"):
        self.user_id1=user_id1
        self.user_id2=user_id2
        self.status=status
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "DL", "friends.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def load_friend(self,user_id):
        friend_list=FriendLinkedList()
        if not os.path.exists(self.file_path):
            return friend_list
        
        with open(self.file_path,"r") as f:
            try:
                data=json.load(f)
            except:
                data={"friendships":[]}
        
        for fr in data["friendships"]:
            if fr["status"]=="accepted" and (fr["user_id1"]==user_id or fr["user_id2"]==user_id):
                if fr["user_id1"]==user_id:
                    friend_id=fr["user_id2"]
                else:
                    friend_id=fr["user_id1"]
                friend_name = fr.get("friend_name", f"User {friend_id}")
                friend_list.add_friend(friend_id,friend_name)
        
        return friend_list
    
    def send_request(self,user_id1,user_id2):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    data = {"friendships": []}
        else:
            data = {"friendships": []}

        # Check if a request already exists
        for fr in data["friendships"]:
            if (fr["user_id1"] == user_id1 and fr["user_id2"] == user_id2) or \
               (fr["user_id1"] == user_id2 and fr["user_id2"] == user_id1):
                print("Request already exists!")
                return False

        # Add new request
        new_request = {
            "user_id1": user_id1,
            "user_id2": user_id2,
            "status": "pending"
        }
        data["friendships"].append(new_request)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Friend request sent from {user_id1} to {user_id2}")
        return True

    def accept_freind_request(self,user_id1,user_id2):
        if not os.path.exists(self.file_path):
            print("File do not exisits")
            return False

        with open(self.file_path,"r") as f:
            try:
                data=json.load(f)
            except:
                data={"Friendships":[]}
        
        updated=False
        for fr in data["friendships"]:
            if fr["user_id1"]==user_id1 and fr["user_id2"]==user_id2 and fr["status"]=="pending":
                fr["status"]="accepted"
                updated=True

        if not updated:
            print("No pending request found between the two user")
            return False

        else:
            with open(self.file_path,"w") as f:
                json.dump(data,f,indent=4)
            return True
            

    def reject_freind_request(self,user_id1,user_id2):
        if not os.path.exists(self.file_path):
            print("File do not exisits")
            return False

        with open(self.file_path,"r") as f:
            try:
                data=json.load(f)
            except:
                data={"Friendships":[]}
        
        updated=False
        for fr in data["friendships"]:
            if fr["user_id1"]==user_id1 and fr["user_id2"]==user_id2 and fr["status"]=="pending":
                fr["status"]="rejected"
                updated=True

        if not updated:
            print("No pending request found between the two user")
            return False

        else:
            with open(self.file_path,"w") as f:
                json.dump(data,f,indent=4)
            return True
           
    def view_pending_requests(self, user_id):
        pending = []

        if not os.path.exists(self.file_path):
            return pending
        
        with open(self.file_path, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {"friendships": []}

        for fr in data["friendships"]:
            if fr["status"] == "pending" and fr["user_id2"] == user_id:
                pending.append(fr["user_id1"])  # who sent the request
        
        return pending

    def get_all_relationships(self, user_id):
        """
        Returns a list of user_ids that have any relationship with the current user
        (accepted, pending, rejected).
        """
        relationships = set()
        if not os.path.exists(self.file_path):
            return relationships
        
        with open(self.file_path, "r") as f:
            try:
                data = json.load(f)
            except:
                data = {"friendships": []}
    
        for fr in data.get("friendships", []):
            if fr["user_id1"] == user_id:
                relationships.add(fr["user_id2"])
            elif fr["user_id2"] == user_id:
                relationships.add(fr["user_id1"])
        
        return relationships
    
