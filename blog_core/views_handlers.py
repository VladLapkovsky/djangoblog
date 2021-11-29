"""This module provides handlers for the blog_core views."""


def get_slug_from_title(title: str) -> str:
    """Reformat post title to post slug".

    Args:
        title (str): post title

    Returns:
        post slug
    """
    return title.strip('*!., ').lower().replace("'", '').replace(' ', '-')
