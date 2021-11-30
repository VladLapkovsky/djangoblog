"""This module provides handlers for the blog_core views."""
from typing import Optional

from pydantic import BaseModel, validator

from blog_core.models import Post


class NewPostContent(BaseModel):
    """pydantic model to check new post data."""

    title: str
    content: Optional[str]

    @validator('title', pre=True)
    def check_title_len(cls, input_title: str):
        """Check title len.

        Args:
            input_title: input title

        Returns:
            input title

        Raises:
            ValueError: if title is too long
        """
        if len(input_title) > 50:
            raise ValueError('The title is longer than 50 characters.')
        return input_title

    @validator('title', pre=True)
    def check_title_correctness(cls, input_title: str):
        """Check title correctness.

        Args:
            input_title: input title

        Returns:
            input title

        Raises:
            ValueError: if title contains not only letters or letters and digits
        """
        if input_title.isalpha() or input_title.isalnum() and not input_title.isdigit():
            raise ValueError('The title should contain letters or letters and digits only.')
        return input_title

    @validator('title')
    def is_post_title_unique(cls, input_title: str):
        """Check title uniqueness.

        Args:
            input_title: input title

        Returns:
            input title

        Raises:
            ValueError: if title is not unique
        """
        if Post.objects.filter(title=input_title).exists():
            raise ValueError('The post with this title is already exists. Try another one.')
        if Post.objects.filter(slug=get_slug_from_title(input_title)).exists():
            raise ValueError('The post with this title is already exists. Try another one.')
        return input_title


def get_slug_from_title(title: str) -> str:
    """Reformat post title to post slug".

    Args:
        title (str): post title

    Returns:
        post slug
    """
    return title.strip('., ').lower().replace("'", '').replace(' ', '-')
