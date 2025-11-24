import customtkinter as ctk

class PostPage:
    def __init__(self, master, current_user, on_create_post, on_edit_post, on_delete_post, on_undo_post, on_get_posts):
        self.master = master
        self.current_user = current_user
        self.on_create_post = on_create_post
        self.on_edit_post = on_edit_post
        self.on_delete_post = on_delete_post
        self.on_undo_post = on_undo_post
        self.on_get_posts = on_get_posts

        # ---------- MAIN FRAME ----------
        self.frame = ctk.CTkFrame(master, fg_color="#1a1a1a")
        self.frame.pack(fill="both", expand=True)

        # ---------- CREATE POST BOX ----------
        self.create_post_frame = ctk.CTkFrame(self.frame, fg_color="#2b2b2b", corner_radius=10)
        self.create_post_frame.pack(pady=20, padx=20, fill="x")

        self.title_label = ctk.CTkLabel(
            self.create_post_frame,
            text=f"What's on your mind, {self.current_user.username}?",
            font=("Segoe UI", 16)
        )
        self.title_label.pack(pady=(10,5), padx=10, anchor="w")

        self.post_entry = ctk.CTkEntry(
            self.create_post_frame,
            placeholder_text="Write something...",
            width=500
        )
        self.post_entry.pack(pady=10, padx=10, fill="x")

        self.post_button = ctk.CTkButton(
            self.create_post_frame,
            text="Post",
            fg_color="orange",
            hover_color="#c77000",
            command=self.create_post
        )
        self.post_button.pack(pady=(0,10), padx=10, anchor="e")

        # ---------- FOOTER (ALWAYS VISIBLE) ----------
        self.footer = ctk.CTkFrame(self.frame, fg_color="#1a1a1a")
        self.footer.pack(side="bottom", fill="x")

        # Undo button always visible
        self.undo_btn = ctk.CTkButton(
            self.footer,
            text="Undo Last Delete",
            fg_color="green",
            width=200,
            command=self.on_undo_post
        )
        self.undo_btn.pack(pady=5)

        # ---------- POSTS LIST (SCROLLABLE) ----------
        self.posts_container = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="#1a1a1a",
            corner_radius=10
        )
        self.posts_container.pack(fill="both", expand=True, padx=20, pady=(0,20))

    # -------------------------------------------------------------------
    # CREATE POST
    # -------------------------------------------------------------------
    def create_post(self):
        content = self.post_entry.get()
        if not content.strip():
            print("Post cannot be empty")
            return
        
        self.post_entry.delete(0, "end")
        self.on_create_post(content)

    # -------------------------------------------------------------------
    # LOAD POSTS
    # -------------------------------------------------------------------
    def load_posts(self, posts):
        for widget in self.posts_container.winfo_children():
            widget.destroy()

        posts = sorted(posts, key=lambda p: p.timestamp, reverse=True)
        for post in posts:
            self.create_post_card(post)

    # -------------------------------------------------------------------
    # CREATE INDIVIDUAL POST CARD
    # -------------------------------------------------------------------
    def create_post_card(self, post):
        card = ctk.CTkFrame(self.posts_container, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", pady=10, padx=10)

        user_label = ctk.CTkLabel(card, text=post.user.username, font=("Segoe UI", 14, "bold"))
        user_label.pack(anchor="w", padx=10, pady=(10, 0))

        content_label = ctk.CTkLabel(card, text=post.content, font=("Segoe UI", 13), wraplength=550)
        content_label.pack(anchor="w", padx=10, pady=5)

        time_label = ctk.CTkLabel(card, text=str(post.timestamp).split(".")[0],
                                  font=("Segoe UI", 11), text_color="gray")
        time_label.pack(anchor="w", padx=10, pady=(0, 10))

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(anchor="e", pady=(0,10), padx=10)

        edit_btn = ctk.CTkButton(btn_frame, text="Edit", width=60,
                                 fg_color="#4a90e2", command=lambda: self.edit_post_ui(post))
        edit_btn.grid(row=0, column=0, padx=5)

        delete_btn = ctk.CTkButton(btn_frame, text="Delete", width=60,
                                   fg_color="#e04a4a", command=lambda: self.on_delete_post(post.post_id))
        delete_btn.grid(row=0, column=1, padx=5)

    # -------------------------------------------------------------------
    # EDIT POST
    # -------------------------------------------------------------------
    def edit_post_ui(self, post):
        edit_win = ctk.CTkToplevel()
        edit_win.title("Edit Post")
        edit_win.geometry("400x250")
        edit_win.grab_set()
        edit_win.focus_force()

        entry = ctk.CTkEntry(edit_win, width=350)
        entry.insert(0, post.content)
        entry.pack(pady=20)

        def confirm():
            new_content = entry.get()
            self.on_edit_post(post.post_id, new_content)
            edit_win.destroy()

        save_btn = ctk.CTkButton(edit_win, text="Save", command=confirm)
        save_btn.pack(pady=10)
