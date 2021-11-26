from django.urls import path

from blog_core.views import AddPostPage, BlogHome, LoginUser, logout_user, RegisterUser, SinglePost

urlpatterns = [
    path('', BlogHome.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('add-post/', AddPostPage.as_view(), name='add_post'),
    path('logout/', logout_user, name='logout'),
    path('<slug:post_slug>/', SinglePost.as_view(), name='post'),
]
