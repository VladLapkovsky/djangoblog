from django.urls import path

from blog_core.views import add_post
from blog_core.views import show_home
from blog_core.views import show_post

urlpatterns = [
    path('add-post/', add_post, name='add_post'),
    path('<slug:post_slug>/', show_post, name='post'),
    path('', show_home, name='home'),
]
