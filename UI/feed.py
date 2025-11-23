import customtkinter as ctk
import random

class FeedPage:
    def __init__(self, master, current_user, post_manager):
        self.master = master
        self.current_user = current_user
        self.post_manager = post_manager

        # Main feed frame
        self.frame = ctk.CTkFrame(master, fg_color="#1a1a1a")
        self.frame.pack(fill="both", expand=True)

        # ------------------- TOP BAR: Search + Sort + New Post -------------------
        top_bar = ctk.CTkFrame(self.frame, fg_color="#2b2b2b", corner_radius=10)
        top_bar.pack(fill="x", padx=20, pady=15)

        self.search_entry = ctk.CTkEntry(top_bar, placeholder_text="Search posts...")
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        search_btn = ctk.CTkButton(top_bar, text="Search", command=self.search_posts, fg_color="#4a90e2")
        search_btn.grid(row=0, column=1, padx=10)

        trending_btn = ctk.CTkButton(top_bar, text="Sort: Trending", command=self.sort_trending, fg_color="orange")
        trending_btn.grid(row=0, column=2, padx=10)


        refresh_btn = ctk.CTkButton(top_bar, text="Refresh Feed", command=self.load_feed)
        refresh_btn.grid(row=0, column=3, padx=10)

        # ------------------- FEED SCROLL AREA -------------------
        self.feed_container = ctk.CTkScrollableFrame(self.frame, fg_color="#1a1a1a")
        self.feed_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Load feed first time
        self.load_feed()

    # ------------------- LOAD FEED -------------------
    def load_feed(self):
        posts = self.post_manager.get_all_posts()

        # Clear previous feed
        for widget in self.feed_container.winfo_children():
            widget.destroy()

        for post in posts:
            self.create_feed_card(post)


    # ------------------- SEARCH POSTS -------------------
    def search_posts(self):
        keyword = self.search_entry.get().strip().lower()
        # if keyword == "":
        #     self.load_feed()
        #     return

        results = self.post_manager.search_post(keyword)

        for widget in self.feed_container.winfo_children():
            widget.destroy()

        for post in results:
            self.create_feed_card(post)

    # ------------------- SORT TRENDING POSTS -------------------
    def sort_trending(self):
        posts = self.post_manager.sort_by_trending()

        for widget in self.feed_container.winfo_children():
            widget.destroy()

        for post in posts:
            self.create_feed_card(post)

    # # ------------------- CREATE FEED POST CARD -------------------
    

    def create_feed_card(self, post):  # <- must be inside class
        card = ctk.CTkFrame(self.feed_container, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", pady=10, padx=10)

        # ------------------- USER INFO FRAME -------------------
        user_frame = ctk.CTkFrame(card, fg_color="transparent")
        user_frame.pack(fill="x", padx=10, pady=(10,0))

        # Random color for avatar
        color = "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])
        avatar = ctk.CTkLabel(user_frame, text=post.user.username[0].upper(), width=30, height=30,
                              fg_color=color, corner_radius=15, font=("Segoe UI", 14, "bold"))
        avatar.pack(side="left")

        user_label = ctk.CTkLabel(user_frame, text=post.user.username, font=("Segoe UI", 14, "bold"))
        user_label.pack(side="left", padx=10)

        # ------------------- POST CONTENT -------------------
        content_label = ctk.CTkLabel(card, text=post.content, font=("Segoe UI", 13), wraplength=550)
        content_label.pack(anchor="w", padx=10, pady=5)

        # ------------------- LIKES & COMMENTS TOGGLE -------------------
        likes_comments_label = ctk.CTkLabel(
            card,
            text=f"❤️ {post.likes}   💬 {post.comment_count}",
            font=("Segoe UI", 12),
            cursor="hand2"
        )
        likes_comments_label.pack(anchor="w", padx=10)

        # ------------------- COMMENTS FRAME (hidden by default) -------------------
        comments_frame = ctk.CTkFrame(card, fg_color="transparent")
        comments_frame.pack(fill="x", padx=10, pady=(5,5))
        comments_frame.pack_forget()  # hide initially

        # ------------------- BUTTON FRAME -------------------
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(anchor="e", padx=10, pady=10)

        like_btn = ctk.CTkButton(
            btn_frame,
            text="Like",
            fg_color="#e04a4a",
            width=60,
            command=lambda: self.like_post(post, likes_comments_label)
        )
        like_btn.grid(row=0, column=0, padx=5)

        comment_btn = ctk.CTkButton(
            btn_frame,
            text="Comment",
            fg_color="#4a90e2",
            width=80,
            command=lambda: self.show_comment_box(card, post, comments_frame)
        )
        comment_btn.grid(row=0, column=1, padx=5)

        # ------------------- TOGGLE COMMENTS FUNCTION -------------------
        def toggle_comments(event=None):
            if comments_frame.winfo_ismapped():
                comments_frame.pack_forget()
            else:
                comments_frame.pack(fill="x", padx=10, pady=(5,5))

                # Clear existing to prevent duplicates
                for child in comments_frame.winfo_children():
                    child.destroy()

                # Show all comments with avatar
                for comment in post.comments:
                    c_frame = ctk.CTkFrame(comments_frame, fg_color="transparent")
                    c_frame.pack(fill="x", pady=2)

                    c_color = "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])
                    c_avatar = ctk.CTkLabel(c_frame, text=comment.user.username[0].upper(),
                                            width=20, height=20, fg_color=c_color, corner_radius=10,
                                            font=("Segoe UI", 10, "bold"))
                    c_avatar.pack(side="left")

                    c_label = ctk.CTkLabel(c_frame, text=f"{comment.user.username}: {comment.text}",
                                            font=("Segoe UI", 12), anchor="w")
                    c_label.pack(side="left", padx=5)

        likes_comments_label.bind("<Button-1>", toggle_comments)


    def show_comment_box(self, card, post, comments_frame):
    # Disable button if box already exists
        for child in card.winfo_children():
            if isinstance(child, ctk.CTkEntry):
                return

        comment_entry = ctk.CTkEntry(card, placeholder_text="Write a comment...")
        comment_entry.pack(fill="x", padx=10, pady=(0,5))

        ok_btn = ctk.CTkButton(card, text="OK", width=50, 
                                command=lambda: self.add_comment(post, comment_entry, comments_frame))
        ok_btn.pack(anchor="e", padx=10, pady=(0,5))

    def add_comment(self, post, entry_widget, comments_frame):
        text = entry_widget.get().strip()
        if text:
            self.post_manager.add_comment_to_post(post.post_id, self.current_user, text)

            # Add comment to UI
            c_label = ctk.CTkLabel(
                comments_frame, 
                text=f"{self.current_user.username}: {text}",
                font=("Segoe UI", 12), anchor="w"
            )
            c_label.pack(fill="x", pady=2)

            # Update likes/comments label
            for widget in comments_frame.master.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "❤️" in widget.cget("text"):
                    widget.configure(text=f"❤️ {post.likes}   💬 {post.comment_count}")


    def like_post(self, post,likes_label):
        self.post_manager.like_post(post)
        likes_label.configure(text=f"❤️ {post.likes}")
    
