from .models import Donation, TwitchUser


def donate2usd(amount, currency, upd_rate={}):
    if type(amount) == str:
        amount = float(amount.replace(',', '.'))
    rate = dict(
        RUB=66,
        UAH=27,
        EUR=1.13,
        USD=1,
    )
    if upd_rate:
        rate.update(upd_rate)
    if currency == 'EUR': # rate bicycle
        return amount * rate.get(currency, 0)
    try:
        return amount / rate.get(currency, 0)
    except ZeroDivisionError:
        return 0


def top_donation_list():
    from django.db.models import Sum, Max
    return Donation.objects.select_related('user').values('user__name').annotate(usd_sum=Sum('amount_usd')).order_by('-usd_sum')
