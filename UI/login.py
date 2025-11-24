import customtkinter as ctk

class LoginPage:
    def __init__(self, master, on_signup, on_login):
        self.master = master
        self.on_signup = on_signup
        self.on_login = on_login

        master.geometry("900x650")
        ctk.set_appearance_mode("dark")

        BG_COLOR = "#0E0E0E"

        # -------- MAIN BACKGROUND --------
        self.frame = ctk.CTkFrame(master, fg_color=BG_COLOR)
        self.frame.pack(fill="both", expand=True)

        # -------- CENTER CONTENT --------
        self.center_frame = ctk.CTkFrame(self.frame, fg_color=BG_COLOR)
        self.center_frame.place(relx=0.5, rely=0.55, anchor="center")

        # -------- TITLE --------
        title = ctk.CTkLabel(
            self.center_frame,
            text="Welcome Back",
            font=("Segoe UI Black", 36),
            text_color="#FF8C00"
        )
        title.pack(pady=(10, 20))

        subtitle = ctk.CTkLabel(
            self.center_frame,
            text="Login to continue your journey!",
            font=("Segoe UI", 15),
            text_color="#BFBFBF"
        )
        subtitle.pack(pady=(0, 25))

        # -------- INPUT FIELDS --------
        self.email = self.create_styled_input("📧", "Enter Email")
        self.password = self.create_styled_input("🔒", "Enter Password", show="*")

        # -------- LOGIN BUTTON --------
        login_btn = ctk.CTkButton(
            self.center_frame,
            text="Login",
            fg_color="#FF8C00",
            hover_color="#E67E00",
            text_color="black",
            width=260,
            height=48,
            font=("Segoe UI Semibold", 17),
            corner_radius=15,
            command=self.action_login
        )
        login_btn.pack(pady=25)

        # -------- SIGNUP BUTTON --------
        signup_btn = ctk.CTkButton(
            self.center_frame,
            text="Don't have an account? Sign Up",
            font=("Segoe UI", 14),
            fg_color="transparent",
            hover_color="#2A2A2A",
            text_color="#FF8C00",
            command=self.on_click_signup
        )
        signup_btn.pack(pady=5)

    # ======================================================================
    #        ⭐ SAME PROFESSIONAL INPUT FIELD AS SIGNUP PAGE ⭐
    # ======================================================================
    def create_styled_input(self, icon, placeholder, show=""):
        container = ctk.CTkFrame(
            self.center_frame,
            fg_color="#1A1A1A",
            corner_radius=15,
            width=330,
            height=55
        )
        container.pack(pady=8)
        container.pack_propagate(False)

        # Icon
        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=("Segoe UI Symbol", 20),
            text_color="#FF8C00",
            width=45
        )
        icon_label.pack(side="left", padx=(10, 5))

        # Entry
        entry = ctk.CTkEntry(
            container,
            placeholder_text=placeholder,
            font=("Segoe UI", 15),
            width=260,
            height=45,
            corner_radius=12,
            border_width=0,
            fg_color="#262626",
            text_color="white",
            placeholder_text_color="#757575",
            show=show
        )
        entry.pack(side="left", fill="x", padx=5, pady=6)

        return entry

    # -------- NAVIGATION FUNCTIONS --------
    def on_click_signup(self):
        self.on_signup()

    def action_login(self):
        email = self.email.get()
        password = self.password.get()
        self.on_login(email, password)
