import re
import os
import json
class User:

    def __init__(self,id,username="",email="",password="",first_name="",last_name="",country="",bio=""):
        self.username=username
        self.id=id
        self.email=email
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.country=country
        self.bio=bio

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def create_and_save_user(username,email,password):
        if not username or username.strip()=="" or not password or password.strip()=="" or not email or email.strip()=="":
            raise ValueError("All fields are required")
        if len(username)<5:
            raise ValueError("Username must be atleast 5 charecters long")
        if len(password)<8:
            raise ValueError("Password must be atleast 8 charecters long")
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
       
        
        project_root = os.path.dirname(os.path.dirname(__file__))  # one level up from BL folder
        dl_folder = os.path.join(project_root, "DL")
        os.makedirs(dl_folder, exist_ok=True)  # make sure DL folder exists
        file_path = os.path.join(dl_folder, "user.json")
        if os.path.exists(file_path):
            with open(file_path,"r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"users": []}  # file is empty or invalid
        else:
            data={"users":[]}   
        
        new_id=max((u["id"] for u in data["users"]),default=0)

        user=User(new_id+1,username,email,password)

        data["users"].append(user.to_dict())

        with open(file_path,"w") as f:
            json.dump(data,f,indent=4)
    
    @staticmethod
    def checkUser(email,password):
        project_root = os.path.dirname(os.path.dirname(__file__))  # one level up from BL folder
        dl_folder = os.path.join(project_root, "DL")
        os.makedirs(dl_folder, exist_ok=True)  # make sure DL folder exists
        file_path = os.path.join(dl_folder, "user.json")
        

        if not os.path.exists(file_path):
            return False

        try:
            with open(file_path,"r") as f:
                try:
                    data=json.load(f)
                except:
                    return False
        except:
            return False
        
        for u in data["users"]:
            if u["email"]==email and u["password"]==password:
                return True
        
        return False
    
    @staticmethod
    def find_user(email):
        project_root = os.path.dirname(os.path.dirname(__file__))  # one level up from BL folder
        dl_folder = os.path.join(project_root, "DL")
        os.makedirs(dl_folder, exist_ok=True)  # make sure DL folder exists
        file_path = os.path.join(dl_folder, "user.json")

        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path,"r") as f:    
                data=json.load(f)

        except Exception as e:
            raise ValueError("Error : ",e)
        
        for u in data["users"]:
            if u["email"]==email:
                return User(
                    u["id"],
                    u["email"],
                    u["password"],
                    u["username"],
                    u.get("first_name",""),
                    u.get("last_name",""),
                    u.get("country",""),
                    u.get("bio","")
                )
        
        return None

    @staticmethod
    def update_user(id,first_name,last_name,country,bio):
        project_root = os.path.dirname(os.path.dirname(__file__))  # one level up from BL folder
        dl_folder = os.path.join(project_root, "DL")
        os.makedirs(dl_folder, exist_ok=True)  # make sure DL folder exists
        file_path = os.path.join(dl_folder, "user.json")

        if not os.path.exists(file_path):
            return False

        with open(file_path,"r") as f:
            try:
                data=json.load(f)
            except:
                json.JSONDecodeError
                data={"users":[]}
        
        for u in data["users"]:
            if u["id"]==id:
                if first_name is not None:
                    u["first_name"]=first_name
                if last_name is not None:
                    u["last_name"]=last_name
                if country is not None:
                    u["country"]=country
                if bio is not None:
                    u["bio"]=bio
                
        with open(file_path,"w") as f:
            json.dump(data,f,indent=4)
            return True
        
        return False
                
    