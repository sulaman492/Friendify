import customtkinter as ctk

class FriendsPage:
    def __init__(self, master, current_user, friend_manager, all_users, on_send_request=None):
        self.master = master
        self.current_user = current_user
        self.friend_manager = friend_manager
        self.all_users = all_users
        self.on_send_request = on_send_request

        # ---------------- MAIN BACKGROUND (Matches Login + Feed) ----------------
        self.frame = ctk.CTkFrame(master, fg_color="#0E0E0E")
        self.frame.pack(fill="both", expand=True)

        # ---------------- TOP BAR ----------------
        top_bar = ctk.CTkFrame(self.frame, fg_color="#1A1A1A", corner_radius=12)
        top_bar.pack(fill="x", padx=20, pady=20)

        view_friends_btn = ctk.CTkButton(
            top_bar,
            text="Friends",
            fg_color="#FF8C00",
            hover_color="#E67A00",
            width=120,
            height=32,
            font=("Segoe UI", 14, "bold"),
            command=self.load_friends
        )
        view_friends_btn.grid(row=0, column=0, padx=10, pady=10)

        view_requests_btn = ctk.CTkButton(
            top_bar,
            text="Requests",
            fg_color="#262626",
            text_color="#FF8C00",
            hover_color="#333333",
            border_width=1,
            border_color="#FF8C00",
            width=120,
            height=32,
            font=("Segoe UI", 14, "bold"),
            command=self.load_requests
        )
        view_requests_btn.grid(row=0, column=1, padx=10, pady=10)

        refresh_btn = ctk.CTkButton(
            top_bar,
            text="Refresh",
            fg_color="#262626",
            text_color="#FF8C00",
            hover_color="#333333",
            border_width=1,
            border_color="#FF8C00",
            width=120,
            height=32,
            font=("Segoe UI", 14),
            command=self.load_all_users
        )
        refresh_btn.grid(row=0, column=2, padx=10, pady=10)

        # ---------------- SCROLL AREA ----------------
        self.container = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="#0E0E0E"
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_all_users()

    # ---------------- CLEAR CONTAINER ----------------
    def clear_feed(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ---------------- LOAD ALL USERS ----------------
    def load_all_users(self):
        self.clear_feed()

        existing_relationships = self.friend_manager.get_all_relationships(self.current_user.id)

        for u in self.all_users:
            if u.id != self.current_user.id and u.id not in existing_relationships:
                self.create_user_card(u)

    # ---------------- USER CARD ----------------
    def create_user_card(self, user):
        card = ctk.CTkFrame(self.container, fg_color="#1A1A1A", corner_radius=12)
        card.pack(fill="x", padx=10, pady=12)

        # Avatar
        initial = user.username[0].upper() if user.username else "?"
        avatar = ctk.CTkLabel(
            card,
            text=initial,
            width=42, height=42,
            corner_radius=20,
            fg_color="#FF8C00",
            text_color="white",
            font=("Segoe UI", 20, "bold")
        )
        avatar.pack(side="left", padx=15)

        # Info frame
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10)

        username_lbl = ctk.CTkLabel(
            info_frame, text=f"@{user.username}",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        username_lbl.pack(anchor="w")

        fullname_lbl = ctk.CTkLabel(
            info_frame, text=f"{user.first_name} {user.last_name}",
            font=("Segoe UI", 14),
            text_color="#DDDDDD"
        )
        fullname_lbl.pack(anchor="w")

        bio_lbl = ctk.CTkLabel(
            info_frame,
            text=user.bio if user.bio else "No bio available",
            font=("Segoe UI", 13),
            text_color="#BBBBBB"
        )
        bio_lbl.pack(anchor="w", pady=(3, 0))

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        send_btn = ctk.CTkButton(
            btn_frame,
            text="Send Request",
            fg_color="#FF8C00",
            hover_color="#E67A00",
            width=120,
            command=lambda: self.send_request_callback(user.id)
        )
        send_btn.pack(pady=5, fill="x")

        ignore_btn = ctk.CTkButton(
            btn_frame,
            text="Ignore",
            fg_color="#B33A3A",
            hover_color="#992F2F",
            width=120,
            command=lambda: card.destroy()
        )
        ignore_btn.pack(pady=5, fill="x")

    # ---------------- LOAD FRIENDS ----------------
    def load_friends(self):
        self.clear_feed()
        friends = self.friend_manager.load_friend(self.current_user.id)

        if not friends.head:
            ctk.CTkLabel(
                self.container,
                text="You have no friends yet.",
                font=("Segoe UI", 14),
                text_color="#AAAAAA"
            ).pack(pady=20)
            return

        temp = friends.head
        while temp:
            user_obj = next((u for u in self.all_users if u.id == temp.friend_id), None)
            if user_obj:
                self.create_friend_card_ui(user_obj)
            temp = temp.next

    # ---------------- FRIEND CARD UI ----------------
    def create_friend_card_ui(self, user):
        card = ctk.CTkFrame(self.container, fg_color="#1A1A1A", corner_radius=12)
        card.pack(fill="x", padx=10, pady=12)

        initial = user.username[0].upper() if user.username else "?"
        avatar = ctk.CTkLabel(
            card,
            text=initial,
            width=42, height=42,
            corner_radius=20,
            fg_color="#FF8C00",
            text_color="white",
            font=("Segoe UI", 20, "bold")
        )
        avatar.pack(side="left", padx=15)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10)

        username_lbl = ctk.CTkLabel(
            info_frame, text=f"@{user.username}",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        username_lbl.pack(anchor="w")

        fullname_lbl = ctk.CTkLabel(
            info_frame, text=f"{user.first_name} {user.last_name}",
            font=("Segoe UI", 14),
            text_color="#DDDDDD"
        )
        fullname_lbl.pack(anchor="w")

        bio_lbl = ctk.CTkLabel(
            info_frame,
            text=user.bio if user.bio else "No bio available",
            font=("Segoe UI", 13),
            text_color="#BBBBBB"
        )
        bio_lbl.pack(anchor="w", pady=(3, 0))

    # ---------------- LOAD REQUESTS ----------------
    def load_requests(self):
        self.clear_feed()
        requests = self.friend_manager.view_pending_requests(self.current_user.id)

        if not requests:
            ctk.CTkLabel(
                self.container,
                text="No pending friend requests.",
                font=("Segoe UI", 14),
                text_color="#AAAAAA"
            ).pack(pady=20)
            return

        for uid in requests:
            self.create_request_card(uid)

    # ---------------- REQUEST CARD ----------------
    def create_request_card(self, sender_id):
        user = next((u for u in self.all_users if u.id == sender_id), None)
        if not user:
            return

        card = ctk.CTkFrame(self.container, fg_color="#1A1A1A", corner_radius=12)
        card.pack(fill="x", padx=10, pady=12)

        initial = user.username[0].upper()
        avatar = ctk.CTkLabel(
            card,
            text=initial,
            width=42, height=42,
            corner_radius=20,
            fg_color="#FF8C00",
            text_color="white",
            font=("Segoe UI", 20, "bold")
        )
        avatar.pack(side="left", padx=15)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10)

        username_lbl = ctk.CTkLabel(
            info_frame, text=f"@{user.username}",
            font=("Segoe UI", 16, "bold"),
            text_color="white"
        )
        username_lbl.pack(anchor="w")

        fullname_lbl = ctk.CTkLabel(
            info_frame, text=f"{user.first_name} {user.last_name}",
            font=("Segoe UI", 14),
            text_color="#DDDDDD"
        )
        fullname_lbl.pack(anchor="w")

        bio_lbl = ctk.CTkLabel(
            info_frame,
            text=user.bio if user.bio else "No bio available",
            font=("Segoe UI", 13),
            text_color="#BBBBBB"
        )
        bio_lbl.pack(anchor="w", pady=(3, 0))

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        accept_btn = ctk.CTkButton(
            btn_frame,
            text="Accept",
            fg_color="#FF8C00",
            hover_color="#E67A00",
            width=100,
            command=lambda: self.accept_and_refresh(sender_id)
        )
        accept_btn.pack(pady=5, fill="x")

        ignore_btn = ctk.CTkButton(
            btn_frame,
            text="Ignore",
            fg_color="#B33A3A",
            hover_color="#992F2F",
            width=100,
            command=lambda: self.reject_request_and_refresh(sender_id)
        )
        ignore_btn.pack(pady=5, fill="x")

    # ---------------- REQUEST ACTIONS ----------------
    def reject_request_and_refresh(self, sender_id):
        self.friend_manager.reject_friend_request(sender_id, self.current_user.id)
        self.load_requests()

    def accept_and_refresh(self, sender_id):
        self.friend_manager.accept_friend_request(sender_id, self.current_user.id)
        self.load_requests()

    def send_request_callback(self, receiver_id):
        if self.on_send_request:
            self.on_send_request(self.current_user.id, receiver_id)

        # Remove card immediately
        for card in self.container.winfo_children():
            children = [w for w in card.winfo_children() if isinstance(w, ctk.CTkFrame)]
            if children:
                username_label = children[0].winfo_children()[0]
                username_text = username_label.cget("text")
                if username_text[1:] == self._get_username_by_id(receiver_id):
                    card.destroy()
                    break

    def _get_username_by_id(self, user_id):
        for u in self.all_users:
            if u.id == user_id:
                return u.username
        return ""
