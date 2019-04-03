from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Author


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('title', 'author', 'tag_list', 'bookmark', 'view', 'rating', 'post_url', 'cover_img', 'created_ts', 'description_short')
    list_filter = ('created_at', 'author')
    search_fields = ('tag_list', 'title', 'author__nickname', 'description_text')
    ordering = ['created_at', ]

    def post_url(self, obj):
        return mark_safe('<a href="{}" target="_blank">Open</a>'.format(obj.url))

    def cover_img(self, obj):
        return mark_safe('<a href="{}" target="_blank"><img src="{}" width="256" alt="No cover"></a>'.format(obj.url.replace('#habracut', ''), obj.cover))

    def description_short(self, obj):
        word_count = 32
        short_by_word = ' '.join(obj.description_text.split(' ')[0:word_count])
        return '{} ...'.format(short_by_word)

    def created_ts(self, obj):
        return obj.created_at.strftime('%d/%b/%Y %H:%M:%S')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

    created_ts.admin_order_field = 'created_at'


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
