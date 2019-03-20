from datetime import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete


class CreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(CreatedMixin):
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=8192)

    def __str__(self):
        return self.title


class TwitchUser(models.Model):
    name = models.CharField(max_length=128, unique=True)
    real_name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name


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
    PRIVAT24 = 'Privat24'
    MONO = 'Monobank'
    DALERT = 'DonationAlert'
    SOURCE_CHOICES = (
        (PRIVAT24, PRIVAT24),
        (MONO, MONO),
        (DALERT, DALERT),
    )

    user = models.ForeignKey('TwitchUser', models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(validators=[MinValueValidator(0.1), ], )
    amount_usd = models.FloatField(default=0, blank=True)
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES)
    message = models.TextField(max_length=1024, blank=True)
    source = models.CharField(max_length=16, default=DALERT, choices=SOURCE_CHOICES)
    alert_id = models.PositiveIntegerField(null=True, blank=True)
    alert_ts = models.DateTimeField()

    def __str__(self):
        return '{} {}'.format(self.amount, self.currency)

    class Meta:
        ordering = ['-alert_ts', ]

    @staticmethod
    def get_top():
        from .helper import top_donation_list
        return top_donation_list()


class Subscribe(models.Model):
    user = models.OneToOneField('TwitchUser', models.CASCADE)
    alert_ts = models.DateTimeField()

    class Meta:
        ordering = ['-alert_ts', ]


class DonationAlertEvent(models.Model):
    alert_id = models.PositiveIntegerField(unique=True)
    alert_ts = models.DateTimeField()
    raw_data = JSONField()

    def __str__(self):
        return '{} {}'.format(self.alert_id, self.raw_data)

    class Meta:
        ordering = ['-alert_ts', ]


@receiver(pre_save, sender=Donation)
def amount_in_usd(sender, instance, **kwargs):
    from .helper import donate2usd
    instance.amount_usd = donate2usd(instance.amount, instance.currency)
