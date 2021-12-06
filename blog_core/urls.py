"""blog_core URL configuration."""

from django.urls import path
from blog_core.views import (AddPostPage, BlogHome, CommentCreateView,
                             LoginUser, PostDetailView, PostListView,
                             RegisterUser, SinglePost, UserPage, logout_user)

urlpatterns = [
    path('api/posts/', PostListView.as_view(), name='api_posts'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='api_post'),
    path('api/comments/', CommentCreateView.as_view({'post': 'create'}), name='api_comments'),
    path('', BlogHome.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('add-post/', AddPostPage.as_view(), name='add_post'),
    path('logout/', logout_user, name='logout'),
    path('@<str:author>/', UserPage.as_view(), name='user_page'),
    path('<slug:post_slug>/', SinglePost.as_view(), name='post'),
]
