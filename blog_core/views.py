from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from blog_core.forms import AddPostForm, LoginUserForm, RegisterUserForm
from blog_core.models import Comment, Post
from blog_core.utils import DataMixin


class BlogHome(DataMixin, ListView):
    paginate_by = 40
    model = Post
    template_name = 'blog_core/home.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            title='Pretty blog',
        )
        return context | extra_context

    def get_queryset(self):
        return Post.objects.annotate(Count('comment')).order_by('-published').select_related('author')


class SinglePost(DataMixin, DetailView):
    model = Post
    template_name = 'blog_core/post.html'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            comments=Comment.objects.filter(post=context['post'].pk).order_by('published').select_related('author')
        )
        return context | extra_context

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['post_slug']).select_related('author')


def get_slug_from_title(title: str) -> str:
    return title.strip('*!., ').lower().replace(' ', '-')


class AddPostPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog_core/add_post.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            title='Add post to blog',
        )
        return context | extra_context

    def form_valid(self, form):
        title = form.cleaned_data['title']
        form.instance.slug = get_slug_from_title(title=title)
        return super().form_valid(form)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog_core/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            title='Register',
        )
        return context | extra_context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'blog_core/login.html'
    LOGIN_REDIRECT_URL = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            title='Authorization',
        )
        return context | extra_context


def logout_user(request):
    logout(request)
    return redirect('home')
