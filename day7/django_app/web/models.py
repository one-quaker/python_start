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
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('title', 'author'), )


class Author(models.Model):
    nickname = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.nickname


# class Tag(models.Model):
#     name = models.CharField(max_length=64, unique=True)
#
#     def __str__(self):
#         return self.name
