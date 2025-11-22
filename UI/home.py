import customtkinter as ctk

class HomePage:
    def __init__(self, master,on_profile):
        self.master = master
        self.on_profile=on_profile
        master.geometry("1200x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # ---------- MAIN FRAME ----------
        self.main_frame = ctk.CTkFrame(master, fg_color="black")
        self.main_frame.pack(fill="both", expand=True)

        # ---------- LEFT PANEL ----------
        self.left_panel = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a")
        self.left_panel.place(relx=0, rely=0, relwidth=0.2, relheight=1)

        # Left side buttons
        self.profile_btn = ctk.CTkButton(self.left_panel, text="Profile", fg_color="orange", hover_color="#c77000",command=self.on_click_profile)
        self.profile_btn.pack(pady=20, padx=10, fill="x")

        self.feed_btn = ctk.CTkButton(self.left_panel, text="Feed", fg_color="orange", hover_color="#c77000")
        self.feed_btn.pack(pady=20, padx=10, fill="x")

        self.post_btn = ctk.CTkButton(self.left_panel, text="Post", fg_color="orange", hover_color="#c77000")
        self.post_btn.pack(pady=20, padx=10, fill="x")

        self.friends_btn = ctk.CTkButton(self.left_panel, text="Friends", fg_color="orange", hover_color="#c77000")
        self.friends_btn.pack(pady=20, padx=10, fill="x")

        # ---------- RIGHT PANEL ----------
        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b")
        self.right_panel.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

        # Placeholder content
        self.content_label = ctk.CTkLabel(self.right_panel, text="Welcome to Friendify!", font=("Segoe UI", 24), text_color="orange")
        self.content_label.pack(pady=50)

        # You can later attach commands to buttons to change content_label or load frames
    def on_click_profile(self):
        self.on_profile(self.right_panel)