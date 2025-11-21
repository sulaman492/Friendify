import customtkinter as ctk
from UI.sigup import SignupPage  
from BL import user_bl

def handle_signup(username,email,password):
    try:
        user_bl.User.create_and_save_user(username,email,password)
        print("user created"+{username})
    except Exception as e:
        print("Error",e)

def main():
    root=ctk.CTk()
    signup_page=SignupPage(root,on_signup=handle_signup)
    root.mainloop()

if __name__=="__main__":
    main()