from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Author


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('title', 'author', 'tag_list', 'bookmark', 'view', 'rating', 'post_url', 'cover_img', 'created_at', 'description_short')
    list_filter = ('created_at', 'author')
    search_fields = ('tag_list', 'title', 'author__nickname', 'description_text')
    ordering = ['created_at', ]

    def post_url(self, obj):
        return mark_safe('<a href="{}" target="_blank">Open</a>'.format(obj.url))

    def cover_img(self, obj):
        return mark_safe('<img src="{}" width="256" alt="No cover">'.format(obj.cover))

    def description_short(self, obj):
        return '{} ...'.format(obj.description_text[:128])

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
