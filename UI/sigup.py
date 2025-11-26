import customtkinter as ctk
from PIL import Image, ImageTk
import os

class SignupPage:
    def __init__(self, master, on_signup, on_login):
        self.master = master
        self.on_signup = on_signup
        self.on_login = on_login

        master.geometry("900x650")
        ctk.set_appearance_mode("dark")

        # -------- MAIN COLORS --------
        BG_COLOR = "#0E0E0E"

        # -------- MAIN FRAME --------
        self.frame = ctk.CTkFrame(master, fg_color=BG_COLOR)
        self.frame.pack(fill="both", expand=True)

        # -------- LEFT & RIGHT PANELS --------
        self.left_frame = ctk.CTkFrame(self.frame, fg_color=BG_COLOR, width=450)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(self.frame, fg_color=BG_COLOR, width=450)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # =====================================================================
        #                    ⭐ LEFT SIDE — ONLY CENTERED TITLE
        # =====================================================================

        left_title = ctk.CTkLabel(
            self.left_frame,
            text="Welcome to Friendify 👋",
            font=("Segoe UI Black", 38),
            text_color="#FF8C00"
        )
        left_title.place(relx=0.5, rely=0.5, anchor="center")

        # =====================================================================
        #                       ⭐ RIGHT SIDE CONTENT
        # =====================================================================
        self.center_frame = ctk.CTkFrame(self.right_frame, fg_color=BG_COLOR)
        self.center_frame.place(relx=0.5, rely=0.55, anchor="center")

        # -------- TITLE --------
        title = ctk.CTkLabel(
            self.center_frame,
            text="Join Friendify",
            font=("Segoe UI Black", 36),
            text_color="#FF8C00"
        )
        title.pack(pady=(5, 20))

        subtitle = ctk.CTkLabel(
            self.center_frame,
            text="Create an account to connect with friends!",
            font=("Segoe UI", 15),
            text_color="#BFBFBF"
        )
        subtitle.pack(pady=(0, 30))

        # -------- INPUT FIELDS --------
        self.username = self.create_styled_input("👤", "Enter Username")
        self.email = self.create_styled_input("📧", "Enter Email")
        self.password = self.create_styled_input("🔒", "Enter Password", show="*")
        self.confirm_password = self.create_styled_input("🔒", "Confirm Password", show="*")

        # -------- SIGN UP BUTTON --------
        signup_btn = ctk.CTkButton(
            self.center_frame,
            text="Create Account",
            fg_color="#FF8C00",
            hover_color="#E67E00",
            text_color="black",
            width=260,
            height=48,
            font=("Segoe UI Semibold", 17),
            corner_radius=15,
            command=self.signup_action
        )
        signup_btn.pack(pady=25)

        # -------- LOGIN LINK --------
        login_btn = ctk.CTkButton(
            self.center_frame,
            text="Already have an account? Login",
            font=("Segoe UI", 14),
            text_color="#FF8C00",
            fg_color="transparent",
            hover_color="#2A2A2A",
            command=self.on_login_click
        )
        login_btn.pack(pady=5)

    # ======================================================================
    #           ⭐ INPUT FIELD DESIGN
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

        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=("Segoe UI Symbol", 20),
            text_color="#FF8C00",
            width=45
        )
        icon_label.pack(side="left", padx=(10, 5))

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

    # ======================================================================
    #                     SIGNUP LOGIC
    # ======================================================================
    def signup_action(self):
        email = self.email.get()
        username = self.username.get()
        password = self.password.get().strip()
        confirm_password = self.confirm_password.get().strip()

        if password != confirm_password:
            print("Error: Passwords do not match!")
            return

        self.on_signup(username, email, password)

    def on_login_click(self):
        self.on_login()
