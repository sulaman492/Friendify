import customtkinter as ctk
from PIL import Image
import os

class SignupPage:
    def __init__(self, master, on_signup, on_login):
        self.master = master
        self.on_signup = on_signup
        self.on_login = on_login

        master.geometry("900x650")
        ctk.set_appearance_mode("dark")

        # -------- FULL BACKGROUND --------
        self.frame = ctk.CTkFrame(master, fg_color="black")
        self.frame.pack(fill="both", expand=True)

        # -------- LEFT & RIGHT FRAMES --------
        self.left_frame = ctk.CTkFrame(self.frame, fg_color="black", width=450)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(self.frame, fg_color="black", width=450)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # -------- LEFT IMAGE --------
        image_path = os.path.join("UI", "img", "signup.png")
        original_image = Image.open(image_path)

        # Left frame size
        frame_width, frame_height = 450, 650

        # Preserve aspect ratio
        img_ratio = original_image.width / original_image.height
        frame_ratio = frame_width / frame_height

        if img_ratio > frame_ratio:
            # Image is wider than frame ratio, fit width
            new_width = frame_width
            new_height = int(frame_width / img_ratio)
        else:
            # Image is taller than frame ratio, fit height
            new_height = frame_height
            new_width = int(frame_height * img_ratio)

        resized_image = original_image.resize((new_width, new_height))
        self.image = ctk.CTkImage(resized_image, size=(new_width, new_height))

        img_label = ctk.CTkLabel(
            self.left_frame,
            image=self.image,
            text="",
            fg_color="black"
        )
        # Center the image
        img_label.place(relx=0.5, rely=0.5, anchor="center")

        # -------- RIGHT SIDE CONTENT --------
        self.center_frame = ctk.CTkFrame(self.right_frame, fg_color="black")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # -------- HEADING --------
        title = ctk.CTkLabel(
            self.center_frame,
            text=" Join Friendify ",
            font=("Segoe UI Black", 34),
            text_color="#FF8C00"
        )
        title.pack(pady=(10, 25))

        subtitle = ctk.CTkLabel(
            self.center_frame,
            text="Join our community and connect with friends!",
            font=("Segoe UI", 16),
            text_color="#bbbbbb"
        )
        subtitle.pack(pady=(0, 25))

        self.username = self.create_styled_input("👤", "Enter Username")
        self.email = self.create_styled_input("📧", "Enter Email")
        self.password = self.create_styled_input("🔒", "Enter Password", show="*")
        self.confirm_password = self.create_styled_input("🔒", "Confirm Password", show="*")

        # -------- SIGN UP BUTTON --------
        signup_btn = ctk.CTkButton(
            self.center_frame,
            text="Get Started",
            fg_color="#FF8C00",
            hover_color="#e67e00",
            text_color="black",
            width=250,
            height=45,
            font=("Segoe UI Semibold", 18),
            corner_radius=12,
            command=self.signup_action
        )
        signup_btn.pack(pady=25)

        # -------- LOGIN LINK --------
        login_btn = ctk.CTkButton(
            self.center_frame,
            text="Already have an account? Login",
            font=("Segoe UI", 15),
            text_color="#FF8C00",
            fg_color="transparent",
            hover_color="#333333",
            command=self.on_login_click
        )
        login_btn.pack(pady=5)

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
            text_color="#FF8C00"
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
            placeholder_text_color="#888888",
            show=show
        )
        entry.pack(side="left", padx=5, pady=8)

        return entry

    def signup_action(self):
        email = self.email.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()
        username = self.username.get()
        if password != confirm_password:
            print("Error: Passwords do not match!")
            return
        self.on_signup(username, email, password)

    def on_login_click(self):
        self.on_login()
