from django.contrib import admin

from .models import (
    Answer,
    Label,
    Question,
)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    pass
