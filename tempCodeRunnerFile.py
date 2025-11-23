import customtkinter as ctk
from UI.sigup import SignupPage  
from UI.login import LoginPage
from UI.home import HomePage
from UI.profile import ProfilePage
from UI.post import PostPage
from UI.feed import FeedPage
from BL import user_bl
from BL.post_management import PostManagement

user=None
pm=PostManagement()

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

def handle_edit_post(post_id ,content,post_page):
    pm.edit_post(post_id,content)
    user_posts = [p for p in pm.posts if p.user.id == user.id]
    post_page.load_posts(user_posts)

def handle_create_post(content):
    pm.create_post(user,content) 

def show_login():
    clear_window()
    login_page=LoginPage(root,on_signup=show_signup,on_login=handle_login)

def show_signup():
    clear_window()
    signup_page=SignupPage(root,on_signup=handle_signup,on_login=show_login)

def show_home_page():
    clear_window()
    home_page=HomePage(root,on_profile=show_profile,on_post=show_users_post,on_feed_load=lambda target_frame:show_feed(target_frame))

def show_feed(target_frame):
    for widget in target_frame.winfo.children():
        widget.destroy()
    feed_page=FeedPage(target_frame,user,pm)

def show_profile(target_frame):
    for widget in target_frame.winfo_children():
        widget.destroy()
    profile_page=ProfilePage(target_frame,user,on_save=handle_profile_save)

def show_users_post(target_frame):
    for widget in target_frame.winfo_children():
        widget.destroy()
    post_page=PostPage(target_frame,user,on_create_post=handle_create_post,on_edit_post=lambda post_id, new_content: handle_edit_post(post_id, new_content, post_page))
    user_posts = [p for p in pm.posts if p.user.id == user.id]
    post_page.load_posts(user_posts)
    
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