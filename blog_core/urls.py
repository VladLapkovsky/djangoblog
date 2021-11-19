from django.urls import path

from blog_core.views import show_home, show_post

urlpatterns = [
    path('<slug:post_slug>/', show_post, name='post'),
    path('', show_home, name='home'),
]
