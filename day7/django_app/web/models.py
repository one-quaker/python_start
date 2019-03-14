import datetime
from django.db import models


class CreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(CreatedMixin):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)

    def __str__(self):
        return self.title


class TwitchUser(models.Model):
    name = models.CharField(max_length=128, unique=True)
    real_name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


class TwitchAction(models.Model):
    user = models.ForeignKey('TwitchUser', models.SET_NULL, null=True, blank=True)
    donation = models.ForeignKey('Donation', models.SET_NULL, null=True, blank=True)
    subscribe = models.BooleanField()
    alert_type = models.PositiveIntegerField()
    alert_id = models.PositiveIntegerField(unique=True)
    alert_ts = models.DateTimeField()

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.subscribe, self.donation)

    class Meta:
        ordering = ['-alert_ts', ]


class Donation(models.Model):
    USD = 'USD'
    EUR = 'EUR'
    BYN = 'BYN'
    KZT = 'KZT'
    RUB = 'RUB'
    UAH = 'UAH'
    BRL = 'BRL'
    CURRENCY_CHOICES = (
        (USD, USD),
        (EUR, EUR),
        (BYN, BYN),
        (KZT, KZT),
        (RUB, RUB),
        (UAH, UAH),
        (BRL, BRL),
    )
    amount = models.FloatField()
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES)
    message = models.TextField(max_length=1024, blank=True)
    alert_id = models.PositiveIntegerField(unique=True)
    alert_ts = models.DateTimeField()

    def __str__(self):
        return '{} {}'.format(self.amount, self.currency)

    class Meta:
        ordering = ['-alert_ts', ]
