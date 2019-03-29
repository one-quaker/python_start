from django.contrib import admin
from .models import Post, Author


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'description')
    list_filter = ('created_at', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
