from django.contrib import admin

from .models import (
    Answer,
    Tag,
    Question,
)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
