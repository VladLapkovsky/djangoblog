"""blog_core URL configuration."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog_core.views import (AddPostPage, BlogHome, CommentCreateView,
                             LoginUser, PostViewSet, RegisterUser, SinglePost,
                             UserPage, logout_user)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='api_posts')
router.register(r'comments', CommentCreateView, basename='api_comments')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', BlogHome.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('add-post/', AddPostPage.as_view(), name='add_post'),
    path('logout/', logout_user, name='logout'),
    path('@<str:author>/', UserPage.as_view(), name='user_page'),
    path('<slug:post_slug>/', SinglePost.as_view(), name='post'),
]