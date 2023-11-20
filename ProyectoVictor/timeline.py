from typing import List, Optional
from post import Post

class Timeline:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.posts: List[Post] = []

    def add_post(self, post: Post):
        self.posts.append(post)

    def remove_post(self, post_id: str):
        self.posts = [p for p in self.posts if p.id != post_id]

    def get_posts(self) -> List[Post]:
        return self.posts

    def get_post_by_id(self, post_id: str) -> Optional[Post]:
        return next((post for post in self.posts if post.id == post_id), None)