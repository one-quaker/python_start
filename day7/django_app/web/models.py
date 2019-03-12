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
