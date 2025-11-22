import customtkinter as ctk

class ProfilePage:
    def __init__(self, master, user,on_save):
        self.master = master
        self.user = user
        self.on_save=on_save

        # MAIN FRAME
        self.frame = ctk.CTkFrame(master, fg_color="black")
        self.frame.pack(fill="both", expand=True)

        # CENTER CONTAINER (Keeps UI centered)
        self.center_frame = ctk.CTkFrame(self.frame, fg_color="#1a1a1a", corner_radius=20)
        self.center_frame.place(relx=0.5, rely=0.1, anchor="n", relwidth=0.6)

        # ---------------- PROFILE IMAGE PLACEHOLDER ----------------
        self.profile_pic = ctk.CTkFrame(
            self.center_frame,
            width=120,
            height=120,
            fg_color="#2b2b2b",
            corner_radius=60  # <-- circle
        )
        self.profile_pic.pack(pady=20)
        
        # Label inside the circle
        pic_label = ctk.CTkLabel(self.profile_pic, text="🙂", font=("Segoe UI", 60))
        pic_label.place(relx=0.5, rely=0.5, anchor="center")

        # ---------------- USER INFO ----------------
        username_label = ctk.CTkLabel(
            self.center_frame,
            text=f"@{self.user.username}",
            font=("Segoe UI Black", 22),
            text_color="orange"
        )
        username_label.pack(pady=(10, 5))

        email_label = ctk.CTkLabel(
            self.center_frame,
            text=self.user.email,
            font=("Segoe UI", 16),
            text_color="#bbbbbb"
        )
        email_label.pack(pady=(0, 20))

        # ---------------- INPUT FIELDS ----------------
        self.first_name = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="First Name",
            width=350
        )
        first=getattr(self.user,"first_name","")
        if first:
            self.first_name.insert(0,first)
        self.first_name.pack(pady=8)
        
        self.last_name = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="Last Name",
            width=350
        )
        last=getattr(self.user,"last_name","")
        if last:
            self.last_name.insert(0,last)
        self.last_name.pack(pady=8)
        
        self.country = ctk.CTkEntry(
        self.center_frame,
        placeholder_text="Country",
        width=350
        )
        country = getattr(self.user, "country", "")
        if country:
            self.country.insert(0, country)
        self.country.pack(pady=8)

        # Bio
        self.bio = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="Bio",
            width=350,
            height=100
        )
        bio = getattr(self.user, "bio", "")
        if bio:
            self.bio.insert(0, bio)
        self.bio.pack(pady=8)
        # ---------------- SAVE BUTTON ----------------
        save_btn = ctk.CTkButton(
            self.center_frame,
            text="Save Profile",
            fg_color="orange",
            hover_color="#c77000",
            height=40,
            width=350,
            command=self.on_click_save
        )
        save_btn.pack(pady=20)

    def on_click_save(self):
        first_name=self.first_name.get()
        last_name=self.last_name.get()
        country=self.country.get()
        bio=self.bio.get()

        self.on_save(first_name,last_name,country,bio)