import customtkinter as ctk
from UI.sigup import SignupPage  
from UI.login import LoginPage
from UI.home import HomePage
from UI.profile import ProfilePage
from BL import user_bl

user=None

def handle_signup(username,email,password):
    try:
        user_bl.User.create_and_save_user(username,email,password)
        global user
        user=user_bl.User.find_user(email)
        show_home_page()
    except Exception as e:
        print("Error",e)

def handle_login(email,password):
    try:
        if user_bl.User.checkUser(email,password):
            global user
            user=user_bl.User.find_user(email)
            show_home_page()
        else:
            print("Invalid username or password",{email},{password})
    except Exception as e:
        print("Error : ",e)

def handle_profile_save(first_name,last_name,country,bio):
    try:
        if user_bl.User.update_user(user.id,first_name,last_name,country,bio):
            print("okay")
    except Exception as e:
        print("Error : ",e)
def show_login():
    clear_window()
    login_page=LoginPage(root,on_signup=show_signup,on_login=handle_login)

def show_signup():
    clear_window()
    signup_page=SignupPage(root,on_signup=handle_signup,on_login=show_login)

def show_home_page():
    clear_window()
    home_page=HomePage(root,on_profile=show_profile)

def show_profile(target_frame):
    for widget in target_frame.winfo_children():
        widget.destroy()
    profile_page=ProfilePage(target_frame,user,on_save=handle_profile_save)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def main():
    global root
    root=ctk.CTk()
    show_signup()
    root.mainloop()

if __name__=="__main__":
    main()