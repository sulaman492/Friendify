import customtkinter as ctk

class LoginPage:
    def __init__(self, master,on_signup,on_login):
        self.master = master
        self.on_signup=on_signup
        self.on_login=on_login

        # Window
        master.geometry("900x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # -------- FULL SCREEN FRAME --------
        self.frame = ctk.CTkFrame(master, fg_color="black")
        self.frame.pack(fill="both", expand=True)

        # CENTER FRAME
        self.center_frame = ctk.CTkFrame(self.frame, fg_color="black")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # -------- TITLE --------
        title = ctk.CTkLabel(
            self.center_frame,
            text="★ Welcome Back ★",
            font=("Segoe UI Black", 34),
            text_color="orange"
        )
        title.pack(pady=(10, 20))

        subtitle = ctk.CTkLabel(
            self.center_frame,
            text="Login to continue your journey!",
            font=("Segoe UI", 16),
            text_color="#bbbbbb"
        )
        subtitle.pack(pady=(0, 25))

        # -------- INPUT FIELDS --------
        self.email = self.create_styled_input("📧", "Enter Email")
        self.password = self.create_styled_input("🔒", "Enter Password", show="*")

        # -------- LOGIN BUTTON --------
        login_btn = ctk.CTkButton(
            self.center_frame,
            text="Login",
            fg_color="orange",
            hover_color="#c77000",
            text_color="black",
            width=250,
            height=45,
            font=("Segoe UI Semibold", 18),
            corner_radius=12,
            command=self.action_login
        )
        login_btn.pack(pady=25)

        # -------- SIGNUP LINK --------
        signup_btn = ctk.CTkButton(
            self.center_frame,
            text="Don't have an account? Sign Up",
            font=("Segoe UI", 15),
            text_color="orange",
            command=self.on_click_signup
        )
        signup_btn.pack(pady=5)

    # -------- INPUT FIELD CREATOR --------
    def create_styled_input(self, icon, placeholder, show=""):
        outer_frame = ctk.CTkFrame(
            self.center_frame,
            fg_color="#1a1a1a",
            corner_radius=15
        )
        outer_frame.pack(pady=10)

        icon_label = ctk.CTkLabel(
            outer_frame,
            text=icon,
            font=("Arial", 20),
            width=40,
            text_color="orange"
        )
        icon_label.pack(side="left", padx=8)

        entry = ctk.CTkEntry(
            outer_frame,
            placeholder_text=placeholder,
            width=280,
            height=45,
            border_width=0,
            corner_radius=10,
            fg_color="#2b2b2b",
            text_color="white",
            placeholder_text_color="#aaaaaa",
            show=show
        )
        entry.pack(side="left", padx=5, pady=8)

        return entry

    def on_click_signup(self):
        self.on_signup()

    def action_login(self):
        email=self.email.get()
        password=self.password.get()

        self.on_login(email,password)
