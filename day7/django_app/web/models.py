from datetime import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField, ArrayField
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete


class CreatedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(CreatedMixin):
    title = models.CharField(max_length=256)
    description_html = models.TextField(max_length=8192)
    description_text = models.TextField(max_length=8192, default='')
    author = models.ForeignKey('Author', related_name='post_list', on_delete=models.SET_NULL, null=True)
    bookmark = models.PositiveIntegerField(default=0)
    comment = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)
    view = models.PositiveIntegerField(default=0)
    cover = models.URLField(max_length=512, default='')
    url = models.URLField(max_length=512, default='')
    tag_list = ArrayField(
        models.CharField(max_length=256, blank=True),
        size=16,
        default=list,
    )

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
