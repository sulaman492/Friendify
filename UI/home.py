import customtkinter as ctk

class HomePage:
    def __init__(self, master, current_user, on_profile, on_post, on_feed_load, on_friends):
        self.master = master
        self.current_user = current_user
        self.on_profile = on_profile
        self.on_post = on_post
        self.on_feed_load = on_feed_load
        self.on_friends = on_friends

        master.geometry("1200x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # ---------- MAIN FRAME ----------
        self.main_frame = ctk.CTkFrame(master, fg_color="black")
        self.main_frame.pack(fill="both", expand=True)

        # ---------- LEFT PANEL (Slightly Wider Dark Sidebar) ----------
        left_width = 0.10
        self.left_panel = ctk.CTkFrame(self.main_frame, fg_color="#0d0d0d")
        self.left_panel.place(relx=0, rely=0, relwidth=left_width, relheight=1)

        # User initial circle at top center
        initial = self.current_user.username[0].upper() if self.current_user.username else "?"
        self.user_circle = ctk.CTkLabel(
            self.left_panel,
            text=initial,
            width=40,
            height=40,
            fg_color="#4a90e2",
            text_color="white",
            corner_radius=100,
            font=("Segoe UI", 18, "bold")
        )
        self.user_circle.pack(pady=10)  # reduced vertical gap

        # Sidebar buttons frame
        self.sidebar_buttons_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.sidebar_buttons_frame.pack(pady=20, fill="y")  # reduced gap

        # Equal width & height for all buttons
        button_width = 70
        button_height = 70
        icon_text_spacing = "\n"

        button_info = [
            ("👤" + icon_text_spacing + "Profile", self.on_click_profile),
            ("📰" + icon_text_spacing + "Feed", lambda: self.on_feed_load(self.right_panel)),
            ("➕" + icon_text_spacing + "Post", self.on_Click_post),
            ("👥" + icon_text_spacing + "Friends", self.friend_action)
        ]

        self.sidebar_buttons = []
        for text, command in button_info:
            btn = ctk.CTkButton(
                self.sidebar_buttons_frame,
                text=text,
                width=button_width,
                height=button_height,
                corner_radius=10,
                fg_color="#1a1a1a",
                hover_color="#333333",
                font=("Segoe UI", 14),
                command=command
            )
            btn.pack(pady=10)
            self.sidebar_buttons.append(btn)

        # ---------- RIGHT PANEL ----------
        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color="#2b2b2b")
        self.right_panel.place(relx=left_width, rely=0, relwidth=1-left_width, relheight=1)  # aligned with left panel

        # Placeholder content
        self.content_label = ctk.CTkLabel(
            self.right_panel,
            text="Welcome to Friendify!",
            font=("Segoe UI", 24),
            text_color="orange"
        )
        self.content_label.pack(pady=50)

        # Load initial feed
        self.on_feed_load(self.right_panel)

    # ------------------ BUTTON CALLBACKS ------------------
    def on_click_profile(self):
        self.on_profile(self.right_panel)

    def on_Click_post(self):
        self.on_post(self.right_panel)

    def friend_action(self):
        self.on_friends(self.right_panel)
