from django.shortcuts import render, get_object_or_404

from blog_core.models import Post


def show_home(request):
    path = 'blog_core/home.html'
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(
        request=request,
        template_name=path,
        context=context,
    )


def show_post(request, post_slug):
    path = 'blog_core/post.html'
    post = get_object_or_404(Post, slug=post_slug)
    context = {'post': post}
    return render(
        request=request,
        template_name=path,
        context=context,
    )
