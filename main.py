import customtkinter as ctk
from UI.sigup import SignupPage  
from UI.login import LoginPage
from BL import user_bl


def handle_signup(username,email,password):
    try:
        user_bl.User.create_and_save_user(username,email,password)
        print("user created",{username})
    except Exception as e:
        print("Error",e)

def handle_login(email,password):
    try:
        if user_bl.User.checkUser(email,password):
            print("login successfull",{email},{password})
        else:
            print("Invalid username or password",{email},{password})
    except Exception as e:
        print("Error : ",e)


def show_login():
    clear_window()
    login_page=LoginPage(root,on_signup=show_signup,on_login=handle_login)

def show_signup():
    clear_window()
    signup_page=SignupPage(root,on_signup=handle_signup,on_login=show_login)


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