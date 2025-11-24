import customtkinter as ctk
import random

class FeedPage:
    def __init__(self, master, current_user, post_manager):
        self.master = master
        self.current_user = current_user
        self.post_manager = post_manager

        # ---------------- BACKGROUND (matches signup/login) ----------------
        self.frame = ctk.CTkFrame(master, fg_color="#0E0E0E")
        self.frame.pack(fill="both", expand=True)

        # ------------------- TOP BAR -------------------
        top_bar = ctk.CTkFrame(
            self.frame,
            fg_color="#1A1A1A",
            corner_radius=12
        )
        top_bar.pack(fill="x", padx=20, pady=20)

        self.search_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="Search posts...",
            fg_color="#262626",
            border_color="#FF8C00"
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        search_btn = ctk.CTkButton(
            top_bar,
            text="Search",
            fg_color="#FF8C00",
            hover_color="#E67A00",
            command=self.search_posts
        )
        search_btn.grid(row=0, column=1, padx=10)

        trending_btn = ctk.CTkButton(
            top_bar,
            text="Trending",
            fg_color="#FF8C00",
            hover_color="#E67A00",
            command=self.sort_trending
        )
        trending_btn.grid(row=0, column=2, padx=10)

        refresh_btn = ctk.CTkButton(
            top_bar,
            text="Refresh Feed",
            fg_color="#262626",
            hover_color="#333333",
            text_color="#FF8C00",
            border_width=1,
            border_color="#FF8C00",
            command=self.load_feed
        )
        refresh_btn.grid(row=0, column=3, padx=10)

        # --------------------- FEED SCROLL AREA -------------------------
        self.feed_container = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="#0E0E0E"
        )
        self.feed_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.load_feed()

    # -------------------------------------------------------------
    def load_feed(self):
        posts = self.post_manager.get_all_posts()

        for widget in self.feed_container.winfo_children():
            widget.destroy()

        for post in posts:
            self.create_feed_card(post)

    # -------------------------------------------------------------
    def search_posts(self):
        keyword = self.search_entry.get().strip().lower()
        results = self.post_manager.search_post(keyword)

        for widget in self.feed_container.winfo_children():
            widget.destroy()

        for post in results:
            self.create_feed_card(post)

    # -------------------------------------------------------------
    def sort_trending(self):
        posts = self.post_manager.sort_by_trending()

        for widget in self.feed_container.winfo_children():
            widget.destroy()

        for post in posts:
            self.create_feed_card(post)

    # -------------------------------------------------------------
    def create_feed_card(self, post):

        card = ctk.CTkFrame(
            self.feed_container,
            fg_color="#1A1A1A",
            corner_radius=14
        )
        card.pack(fill="x", pady=12, padx=10)

        # ---------------- USER HEADER ----------------
        user_frame = ctk.CTkFrame(card, fg_color="transparent")
        user_frame.pack(fill="x", padx=10, pady=(10, 0))

        avatar_color = "#" + "".join(random.choice("0123456789ABCDEF") for _ in range(6))
        avatar = ctk.CTkLabel(
            user_frame,
            text=post.user.username[0].upper(),
            width=35, height=35,
            fg_color=avatar_color,
            corner_radius=18,
            font=("Segoe UI", 14, "bold")
        )
        avatar.pack(side="left")

        user_label = ctk.CTkLabel(
            user_frame,
            text=post.user.username,
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        )
        user_label.pack(side="left", padx=10)

        # ---------------- CONTENT ----------------
        content_label = ctk.CTkLabel(
            card,
            text=post.content,
            font=("Segoe UI", 13),
            wraplength=550,
            text_color="#DDDDDD"
        )
        content_label.pack(anchor="w", padx=10, pady=6)

        # ---------------- LIKE + COMMENTS ----------------
        lc_label = ctk.CTkLabel(
            card,
            text=f"❤️ {post.likes}   💬 {post.comment_count}",
            font=("Segoe UI", 12),
            text_color="#FF8C00",
            cursor="hand2"
        )
        lc_label.pack(anchor="w", padx=10)

        comments_frame = ctk.CTkFrame(card, fg_color="transparent")
        comments_frame.pack(fill="x", padx=10, pady=5)
        comments_frame.pack_forget()

        # ---------------- BUTTONS ----------------
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(anchor="e", padx=10, pady=10)

        like_btn = ctk.CTkButton(
        btn_frame,
        text="Unlike" if self.current_user.username in getattr(post, "liked_users", set()) else "Like",
        fg_color="#C93E3E" if self.current_user.username in getattr(post, "liked_users", set()) else "#E04A4A",
        hover_color="#E04A4A",
        width=70,
        command=lambda: self.toggle_like(post, like_btn, lc_label)
        )
        like_btn.grid(row=0, column=0, padx=5)

        comment_btn = ctk.CTkButton(
            btn_frame,
            text="Comment",
            fg_color="#FF8C00",
            hover_color="#E67A00",
            width=90,
            command=lambda: self.show_comment_box(card, post, comments_frame)
        )
        comment_btn.grid(row=0, column=1, padx=5)

        # ---------------- TOGGLE COMMENTS ----------------
        def toggle_comments(event=None):
            if comments_frame.winfo_ismapped():
                comments_frame.pack_forget()
            else:
                comments_frame.pack(fill="x", padx=10, pady=5)

                for child in comments_frame.winfo_children():
                    child.destroy()

                for comment in post.comments:
                    c_frame = ctk.CTkFrame(comments_frame, fg_color="transparent")
                    c_frame.pack(fill="x", pady=2)

                    c_color = "#" + "".join(random.choice("0123456789ABCDEF") for _ in range(6))
                    c_avatar = ctk.CTkLabel(
                        c_frame,
                        text=comment.user.username[0].upper(),
                        width=25, height=25,
                        fg_color=c_color,
                        corner_radius=12,
                        font=("Segoe UI", 10, "bold")
                    )
                    c_avatar.pack(side="left")

                    c_label = ctk.CTkLabel(
                        c_frame,
                        text=f"{comment.user.username}: {comment.text}",
                        font=("Segoe UI", 12),
                        text_color="#CCCCCC"
                    )
                    c_label.pack(side="left", padx=5)

        lc_label.bind("<Button-1>", toggle_comments)

    # -------------------------------------------------------------
    def show_comment_box(self, card, post, comments_frame):

        # prevent duplicate input boxes
        for child in card.winfo_children():
            if isinstance(child, ctk.CTkEntry):
                return

        comment_entry = ctk.CTkEntry(
            card,
            placeholder_text="Write a comment...",
            fg_color="#262626",
            border_color="#FF8C00",
        )
        comment_entry.pack(fill="x", padx=10, pady=(0, 5))

        ok_btn = ctk.CTkButton(
            card,
            text="OK",
            width=55,
            fg_color="#FF8C00",
            hover_color="#E67A00",
            command=lambda: self.add_comment(post, comment_entry, comments_frame)
        )
        ok_btn.pack(anchor="e", padx=10, pady=(0, 5))

    # -------------------------------------------------------------
    def add_comment(self, post, entry_widget, comments_frame):
        text = entry_widget.get().strip()
        if text:
            # Add comment to backend
            self.post_manager.add_comment_to_post(post.post_id, self.current_user, text)

            # Show comment in the comments_frame
            c_label = ctk.CTkLabel(
                comments_frame,
                text=f"{self.current_user.username}: {text}",
                font=("Segoe UI", 12),
                text_color="#CCCCCC"
            )
            c_label.pack(fill="x", pady=2)

            # Destroy comment entry and OK button
            entry_widget.destroy()
            for child in entry_widget.master.winfo_children():
                if isinstance(child, ctk.CTkButton) and child.cget("text") == "OK":
                    child.destroy()

            # Ensure comments are visible after adding
            comments_frame.pack(fill="x", padx=10, pady=5)

    # -------------------------------------------------------------
    def like_post(self, post, likes_label):
        liked = self.post_manager.like_post(post, self.current_user)
        if liked:
            likes_label.configure(text=f"❤️ {post.likes}   💬 {post.comment_count}")

    def toggle_like(self, post, like_btn, likes_label):
        result = self.post_manager.toggle_like_post(post, self.current_user)
    
        if result == "liked":
            like_btn.configure(text="Unlike", fg_color="#C93E3E")
        else:
            like_btn.configure(text="Like", fg_color="#E04A4A")
    
        likes_label.configure(text=f"❤️ {post.likes}   💬 {post.comment_count}")
    