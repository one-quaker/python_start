from django.contrib import admin
from .models import Post, Author


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('title', 'author', 'tag_list', 'bookmark', 'view', 'rating', 'url', 'cover', 'created_at', 'description_text')
    list_filter = ('created_at', 'author')
    search_fields = ('tag_list', 'title')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
