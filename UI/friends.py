import customtkinter as ctk

class FriendsPage:
    def __init__(self, master, current_user, friend_manager, all_users,on_send_request=None):
        self.master = master
        self.current_user = current_user
        self.friend_manager = friend_manager
        self.all_users = all_users
        self.on_send_request=on_send_request

        # MAIN FRAME
        self.frame = ctk.CTkFrame(master, fg_color="#1a1a1a")
        self.frame.pack(fill="both", expand=True)

        # ------------------- TOP BAR -------------------
        top_bar = ctk.CTkFrame(self.frame, fg_color="#2b2b2b", corner_radius=10)
        top_bar.pack(fill="x", padx=20, pady=15)

        # Only view friends & requests + refresh
        view_friends_btn = ctk.CTkButton(top_bar, text="View Friends", fg_color="green",
                                         command=self.load_friends)
        view_friends_btn.grid(row=0, column=0, padx=10, pady=10)

        view_requests_btn = ctk.CTkButton(top_bar, text="View Requests", fg_color="orange",
                                          command=self.load_requests)
        view_requests_btn.grid(row=0, column=1, padx=10, pady=10)

        refresh_btn = ctk.CTkButton(top_bar, text="Refresh", fg_color="#444444",
                                    command=self.load_all_users)
        refresh_btn.grid(row=0, column=2, padx=10, pady=10)

        # ------------------- SCROLLABLE CONTENT -------------------
        self.container = ctk.CTkScrollableFrame(self.frame, fg_color="#1a1a1a")
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # ------------------- LOAD ALL USERS ON INIT -------------------
        self.load_all_users()

    # ------------------- CLEAR FEED -------------------
    def clear_feed(self):
        for w in self.container.winfo_children():
            w.destroy()

    # ------------------- LOAD ALL USERS -------------------
    def load_all_users(self):
        self.clear_feed()
        # Get all users that already have a relationship with current user
        existing_relationships = self.friend_manager.get_all_relationships(self.current_user.id)

        for u in self.all_users:
            if u.id == self.current_user.id:
                continue
            if u.id in existing_relationships:  # skip users who already have any relationship
                continue
            self.create_user_card(u)


    # ------------------- USER CARD -------------------
    def create_user_card(self, user):
        card = ctk.CTkFrame(self.container, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", padx=10, pady=10)

        # Circle initial
        initial = user.username[0].upper() if user.username else "?"
        circle = ctk.CTkLabel(
            card,
            text=initial,
            width=45,
            height=45,
            fg_color="#4a90e2",
            text_color="white",
            corner_radius=100,
            font=("Segoe UI", 22, "bold")
        )
        circle.pack(side="left", padx=15)

        # User info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10)

        username_lbl = ctk.CTkLabel(info_frame, text=f"@{user.username}", font=("Segoe UI", 16, "bold"))
        username_lbl.pack(anchor="w")

        fullname_lbl = ctk.CTkLabel(info_frame, text=f"{user.first_name} {user.last_name}", font=("Segoe UI", 14))
        fullname_lbl.pack(anchor="w")

        bio_lbl = ctk.CTkLabel(info_frame, text=user.bio if user.bio else "No bio available",
                               font=("Segoe UI", 13), text_color="#cccccc")
        bio_lbl.pack(anchor="w", pady=(3,0))

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        send_btn = ctk.CTkButton(
            btn_frame,
            text="Send Request",
            fg_color="#3b9c3f",
            command=lambda: self.send_request_callback(user.id)
        )
        send_btn.pack(pady=5, fill="x")

        ignore_btn = ctk.CTkButton(
            btn_frame,
            text="Ignore",
            fg_color="#b33a3a",
            command=lambda: card.destroy()
        )
        ignore_btn.pack(pady=5, fill="x")

    # ------------------- LOAD FRIENDS -------------------
    # ------------------- LOAD FRIENDS -------------------
    def load_friends(self):
        self.clear_feed()
        friends = self.friend_manager.load_friend(self.current_user.id)
    
        if not friends.head:
            no_label = ctk.CTkLabel(self.container, text="You have no friends yet.",
                                    font=("Segoe UI", 14))
            no_label.pack(pady=20)
            return
        
        temp = friends.head
        while temp:
            user_obj = next((u for u in self.all_users if u.id == temp.friend_id), None)
            if user_obj:
                self.create_friend_card_ui(user_obj)
            temp = temp.next
    
    # ------------------- FRIEND CARD UI -------------------
    def create_friend_card_ui(self, user):
        card = ctk.CTkFrame(self.container, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", padx=10, pady=10)
    
        # Circle initial
        initial = user.username[0].upper() if user.username else "?"
        circle = ctk.CTkLabel(
            card,
            text=initial,
            width=45,
            height=45,
            fg_color="#4a90e2",
            text_color="white",
            corner_radius=100,
            font=("Segoe UI", 22, "bold")
        )
        circle.pack(side="left", padx=15)
    
        # User info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10)
    
        username_lbl = ctk.CTkLabel(info_frame, text=f"@{user.username}", font=("Segoe UI", 16, "bold"))
        username_lbl.pack(anchor="w")
    
        fullname_lbl = ctk.CTkLabel(info_frame, text=f"{user.first_name} {user.last_name}", font=("Segoe UI", 14))
        fullname_lbl.pack(anchor="w")
    
        bio_lbl = ctk.CTkLabel(info_frame, text=user.bio if user.bio else "No bio available",
                               font=("Segoe UI", 13), text_color="#cccccc")
        bio_lbl.pack(anchor="w", pady=(3,0))
    

    # ------------------- LOAD REQUESTS -------------------
    def load_requests(self):
        self.clear_feed()
        requests = self.friend_manager.view_pending_requests(self.current_user.id)

        if not requests:
            no_label = ctk.CTkLabel(self.container, text="No pending friend requests.",
                                    font=("Segoe UI", 14))
            no_label.pack(pady=20)
            return

        for uid in requests:
            self.create_request_card(uid)

    # ------------------- REQUEST CARD -------------------
    def create_request_card(self, sender_id):
        # Find the user object
        user = next((u for u in self.all_users if u.id == sender_id), None)
        if not user:
            return  # User not found

        card = ctk.CTkFrame(self.container, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", padx=10, pady=10)

        # Circle initial
        initial = user.username[0].upper() if user.username else "?"
        circle = ctk.CTkLabel(
            card,
            text=initial,
            width=45,
            height=45,
            fg_color="#4a90e2",
            text_color="white",
            corner_radius=100,
            font=("Segoe UI", 22, "bold")
        )
        circle.pack(side="left", padx=15)

        # User info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10)

        username_lbl = ctk.CTkLabel(info_frame, text=f"@{user.username}", font=("Segoe UI", 16, "bold"))
        username_lbl.pack(anchor="w")

        fullname_lbl = ctk.CTkLabel(info_frame, text=f"{user.first_name} {user.last_name}", font=("Segoe UI", 14))
        fullname_lbl.pack(anchor="w")

        bio_lbl = ctk.CTkLabel(info_frame, text=user.bio if user.bio else "No bio available",
                               font=("Segoe UI", 13), text_color="#cccccc")
        bio_lbl.pack(anchor="w", pady=(3,0))

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        accept_btn = ctk.CTkButton(
            btn_frame,
            text="Accept",
            fg_color="green",
            width=80,
            command=lambda: self.accept_and_refresh(sender_id)
        )
        accept_btn.pack(pady=5, fill="x")

        ignore_btn = ctk.CTkButton(
            btn_frame,
            text="Ignore",
            fg_color="#b33a3a",
            width=80,
            command=lambda: self.reject_request_and_refresh(sender_id)
        )
        ignore_btn.pack(pady=5, fill="x")

    # ------------------- REJECT REQUEST -------------------
    def reject_request_and_refresh(self, sender_id):
        self.friend_manager.reject_friend_request(sender_id, self.current_user.id)
        self.load_requests()

    def accept_and_refresh(self, sender_id):
    # Call backend to accept the friend request
        self.friend_manager.accept_friend_request(sender_id, self.current_user.id)
        # Refresh the request list to remove the accepted request from UI
        self.load_requests()

    def send_request_callback(self, receiver_id):
        if self.on_send_request:
            # Call the main app callback
            self.on_send_request(self.current_user.id, receiver_id)

        # Remove the user card from UI immediately
        for card in self.container.winfo_children():
            # Each card has a CTkLabel with username inside info_frame
            labels = [w for w in card.winfo_children() if isinstance(w, ctk.CTkFrame)]
            if labels:
                info_frame = labels[0]
                username_label = info_frame.winfo_children()[0]
                username_text = username_label.cget("text")  # e.g., @username
                if username_text[1:] == self._get_username_by_id(receiver_id):
                    card.destroy()
                    break

    def _get_username_by_id(self, user_id):
        # Helper to find username from all_users
        for u in self.all_users:
            if u.id == user_id:
                return u.username
        return ""
