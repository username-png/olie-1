from django.db import models


class Question(models.Model):

    text = models.TextField()
    tag = models.ForeignKey(
        'Tag', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):

    text = models.TextField()
    tag = models.ForeignKey(
        'Tag', blank=True, null=True, on_delete=models.SET_NULL)
    is_suggestion = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class Tag(models.Model):

    slug = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, blank=True, default='')
    description = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.slug}'
