from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from blog_core.forms import AddPostForm
from blog_core.models import Comment, Post
from blog_core.utils import DataMixin

# TODO remove comments


class BlogHome(DataMixin, ListView):
    paginate_by = 3
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
        return Post.objects.annotate(Count('comment')).order_by('-published')

# def show_home(request):
#     path = 'blog_core/home.html'
#     posts = Post.objects.all().annotate(Count('comment')).order_by('-published')
#     context = {'posts': posts, 'is_current_page': "active"}
#     return render(
#         request=request,
#         template_name=path,
#         context=context,
#     )


class SinglePost(DataMixin, DetailView):
    model = Post
    template_name = 'blog_core/post.html'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(
            comments=Comment.objects.filter(post=context['post'].pk).order_by('published')
        )
        return context | extra_context


# def show_post(request, post_slug):
#     path = 'blog_core/post.html'
#     post = get_object_or_404(Post, slug=post_slug)
#     post_comments = Comment.objects.filter(post=post.id).order_by('published')
#     context = {'post': post, 'comments': post_comments}
#     return render(
#         request=request,
#         template_name=path,
#         context=context,
#     )


def get_slug_from_title(title: str) -> str:
    return title.strip('*!., ').lower().replace(' ', '-')


class AddPostPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog_core/add_post.html'
    success_url = reverse_lazy('home')
    login_url = '/admin/'

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


# def add_post(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST)
#         if form.is_valid():
#             new_post = form.save(commit=False)
#             new_post.slug = get_slug_from_title(request.POST['title'])
#             new_post.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     path = 'blog_core/add_post.html'
#     context = {'form': form}
#     return render(
#         request=request,
#         template_name=path,
#         context=context,
#     )
