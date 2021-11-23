from django.urls import path

from blog_core.views import AddPostPage
from blog_core.views import BlogHome
from blog_core.views import SinglePost

urlpatterns = [
    path('add-post/', AddPostPage.as_view(), name='add_post'),
    path('<slug:post_slug>/', SinglePost.as_view(), name='post'),
    path('', BlogHome.as_view(), name='home'),
]
