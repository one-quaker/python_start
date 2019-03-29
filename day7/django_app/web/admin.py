from django.contrib import admin
from .models import Post, Author


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description')
    list_filter = ('author', )


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
