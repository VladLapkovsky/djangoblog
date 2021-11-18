from django.shortcuts import render, get_object_or_404

from blog_core.models import Post, Comment
from django.db.models import Count

def show_home(request):
    path = 'blog_core/home.html'
    posts = Post.objects.all().annotate(Count('comment')).order_by('-published')
    context = {'posts': posts}
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
