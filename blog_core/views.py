"""This module provides views for the blog_core app.

Views:
BlogHome - provides view for the home page.
SinglePost - provides view for the single post page.
AddPostPage - provides view for the add post page.
RegisterUser - provides view for the user register page.
LoginUser - provides view for the user log in page.
logout_user - provides user logout logic.
"""
from typing import Union

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin

from blog_core.forms import AddPostForm, CommentForm, LoginUserForm, RegisterUserForm
from blog_core.models import Comment, Post
from blog_core.utils import DataMixin
from blog_core.views_handlers import get_slug_from_title
from users.models import CustomUser


class BlogHome(DataMixin, ListView):
    """Provide view for the home page."""

    paginate_by = 3
    model = Post
    template_name = 'blog_core/home.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs: dict) -> dict:
        """Provide additional args to the home page template.

        Add page title.

        Args:
            object_list: context kwargs
            **kwargs: context kwargs

        Returns:
            args for the home page template
        """
        context = super().get_context_data(object_list=object_list, **kwargs)
        extra_context = self.get_user_context(
            title='Pretty blog',
        )
        return context | extra_context

    def get_queryset(self) -> QuerySet:
        """Add comment column to the posts objects.

        Returns:
            Post QuerySet with comment column
        """
        return Post.objects.annotate(Count('comment')).order_by('-published').select_related('author')


class SinglePost(DataMixin, DetailView, FormMixin):
    """Provide view for the single post page."""

    model = Post
    template_name = 'blog_core/post.html'
    slug_url_kwarg = 'post_slug'
    form_class = CommentForm
    comments_per_page = 3

    def get_context_data(self, **kwargs: dict) -> dict:
        """Provide comment pagination.

        Args:
            **kwargs: context kwargs

        Returns:
            args for the home page template
        """
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            comments=Comment.objects.filter(post=context['post'].pk).order_by('-published').select_related('author'),
        )
        paginator = Paginator(extra_context['comments'], self.comments_per_page)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)
        return context

    def get_queryset(self) -> QuerySet:
        """Select specific post from the Post model.

        Returns:
            Post QuerySet with specific post
        """
        return Post.objects.filter(slug=self.kwargs['post_slug']).select_related('author')

    def post(self, request: WSGIRequest) -> Union[HttpResponseRedirect, HttpResponse]:
        """Create new comment object from comment form.

        Args:
            request: POST request

        Returns:
            redirect to the same page
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
            Comment.objects.create(
                post=post,
                author=CustomUser.objects.get(id=self.request.user.id),
                content=cleaned_data['content'],
            )
            return HttpResponseRedirect(self.request.get_full_path())
        return render(request, self.template_name, {'form': form})


class AddPostPage(LoginRequiredMixin, DataMixin, CreateView):
    """Provides view for the add post page."""

    form_class = AddPostForm
    template_name = 'blog_core/add_post.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def get_context_data(self, **kwargs: dict) -> dict:
        """Provide additional args to the add post page.

        Add page title.

        Args:
            **kwargs: context kwargs

        Returns:
            args for the add post page
        """
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            title='Add post to blog',
        )
        return context | extra_context

    def form_valid(self, form: AddPostForm) -> HttpResponseRedirect:
        """Add post slug and author_id to the add post form.

        Args:
            form: AddPostForm

        Returns:
            HttpResponseRedirect
        """
        title = form.cleaned_data['title']
        form.instance.slug = get_slug_from_title(title=title)
        form.instance.author = CustomUser.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class RegisterUser(DataMixin, CreateView):
    """Provide view for the user register page."""

    form_class = RegisterUserForm
    template_name = 'blog_core/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs: dict) -> dict:
        """Provide additional args to the user register page.

        Add page title.

        Args:
            **kwargs: context kwargs

        Returns:
            args for the user register page
        """
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            title='Register',
        )
        return context | extra_context

    def form_valid(self, form: RegisterUserForm) -> HttpResponseRedirect:
        """Add automatic user log in after register.

        Args:
            form: AddPostForm

        Returns:
            redirect to the previous page
        """
        user = form.save()
        login(self.request, user)
        return redirect(self.request.GET['next'])


class LoginUser(DataMixin, LoginView):
    """Provide view for the user log in page."""

    form_class = LoginUserForm
    template_name = 'blog_core/login.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        """Provide additional args to the user log in page.

        Add page title.

        Args:
            **kwargs: context kwargs

        Returns:
            args for the user log in page
        """
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            title='Authorization',
        )
        return context | extra_context


def logout_user(request: WSGIRequest) -> HttpResponseRedirect:
    """Provide user logout logic.

    Args:
        request: GET request

    Returns:
            redirect to the same page
    """
    logout(request)
    return redirect(request.GET['next'])
