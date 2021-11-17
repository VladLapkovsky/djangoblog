from django.contrib import admin

from blog_core.models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'content', 'published', 'rating')
    list_display_links = ('title', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'published', 'rating', 'post')
    list_display_links = ('author', 'content')
    search_fields = ('author', 'content')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
