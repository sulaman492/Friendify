import customtkinter as ctk

class ProfilePage:
    def __init__(self, master, user, on_save):
        self.master = master
        self.user = user
        self.on_save = on_save

        # MAIN FRAME
        self.frame = ctk.CTkFrame(master, fg_color="black")
        self.frame.pack(fill="both", expand=True)

        # CENTER CONTAINER
        self.center_frame = ctk.CTkFrame(
            self.frame,
            fg_color="#1a1a1a",
            corner_radius=20
        )
        self.center_frame.place(relx=0.5, rely=0.1, anchor="n", relwidth=0.6)

        # ---------------- PROFILE INITIAL CIRCLE ----------------
        initial = (self.user.username[0].upper() if self.user.username else "?")

        self.profile_pic = ctk.CTkFrame(
            self.center_frame,
            width=120,
            height=120,
            fg_color="#2b2b2b",
            corner_radius=60
        )
        self.profile_pic.pack(pady=20)

        pic_label = ctk.CTkLabel(
            self.profile_pic,
            text=initial,
            font=("Segoe UI", 48, "bold"),
            text_color="white"
        )
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
        first_name_val = getattr(self.user, "first_name", "")
        self.first_name = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="",
            width=350,
            fg_color="#2b2b2b",
            text_color="white"
        )
        if first_name_val:
            self.first_name.insert(0, first_name_val)
        else:
            self.first_name.insert(0, "First Name")
        self.first_name.pack(pady=8)

        last_name_val = getattr(self.user, "last_name", "")
        self.last_name = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="",
            width=350,
            fg_color="#2b2b2b",
            text_color="white"
        )
        if last_name_val:
            self.last_name.insert(0, last_name_val)
        else:
            self.last_name.insert(0, "Last Name")
        self.last_name.pack(pady=8)

        country_val = getattr(self.user, "country", "")
        self.country = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="",
            width=350,
            fg_color="#2b2b2b",
            text_color="white"
        )
        if country_val:
            self.country.insert(0, country_val)
        else:
            self.country.insert(0, "Country")
        self.country.pack(pady=8)

        bio_val = getattr(self.user, "bio", "")
        self.bio = ctk.CTkEntry(
            self.center_frame,
            placeholder_text="",
            width=350,
            height=100,
            fg_color="#2b2b2b",
            text_color="white"
        )
        if bio_val:
            self.bio.insert(0, bio_val)
        else:
            self.bio.insert(0, "Bio")
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
        first_name = self.first_name.get()
        last_name = self.last_name.get()
        country = self.country.get()
        bio = self.bio.get()

        # Update database
        self.on_save(first_name, last_name, country, bio)

        # Update UI fields to reflect saved data
        self.first_name.delete(0, "end")
        self.first_name.insert(0, first_name)

        self.last_name.delete(0, "end")
        self.last_name.insert(0, last_name)

        self.country.delete(0, "end")
        self.country.insert(0, country)

        self.bio.delete(0, "end")
        self.bio.insert(0, bio)
