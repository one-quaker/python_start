from django.contrib import admin
from .models import Post, TwitchUser, TwitchAction, Donation


class TwitchActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'donation', 'subscribe', 'alert_id', 'alert_type', 'alert_ts')
    list_filter = ('user', 'donation', 'subscribe')


class DonationAdmin(admin.ModelAdmin):
    list_display = ('amount', 'currency', 'message', 'alert_ts')
    list_filter = ('amount', 'currency')


admin.site.register(Post)
admin.site.register(TwitchUser)
admin.site.register(TwitchAction, TwitchActionAdmin)
admin.site.register(Donation, DonationAdmin)
