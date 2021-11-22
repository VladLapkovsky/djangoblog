from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

from blog_core.models import Post, Comment
from blog_core.forms import AddPostForm

def show_home(request):
    path = 'blog_core/home.html'
    posts = Post.objects.all().annotate(Count('comment')).order_by('-published')
    context = {'posts': posts, 'is_current_page': "active"}
    return render(
        request=request,
        template_name=path,
        context=context,
    )


def show_post(request, post_slug):
    path = 'blog_core/post.html'
    post = get_object_or_404(Post, slug=post_slug)
    post_comments = Comment.objects.filter(post=post.id).order_by('published')
    context = {'post': post, 'comments': post_comments}
    return render(
        request=request,
        template_name=path,
        context=context,
    )


def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    path = 'blog_core/add_post.html'
    context = {'form': form}
    return render(
        request=request,
        template_name=path,
        context=context,
    )
