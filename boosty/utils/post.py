from boosty.types import Post


def get_post_url(post: Post) -> str:
    """Get post url"""
    return f"https://boosty.to/{post.user.blogUrl}/{post.id}"
