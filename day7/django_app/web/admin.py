from django.contrib import admin
from .models import Post, TwitchUser, Subscribe, Donation, DonationAlertEvent


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'alert_ts')
    list_filter = ('user', 'alert_ts')


class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'amount_usd', 'message', 'alert_ts', 'source', 'alert_id')
    list_filter = ('amount', 'currency', 'source', 'alert_id')


admin.site.register(Post)
admin.site.register(TwitchUser)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationAlertEvent)
