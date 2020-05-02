from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import models
from django.urls import reverse
from django.views.generic.edit import UpdateView

from model.model import (
    model,
    tokenizer,
    tags,
)
from model.tooling import predict

from .forms import QuestionForm
from .models import (
    Question,
    Tag,
)
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PredictView(APIView):

    def get(self, request, format=None):
        question = request.query_params.get('question', '')
        return Response(predict(model, tokenizer, tags, question))


class ClassificationView(UpdateView):
    template_name_suffix = '_update_form'
    form_class = QuestionForm

    def get_object(self):
        return Question.objects.filter(tag__isnull=True).order_by('?').first()

    def get_success_url(self):
        return reverse('questions_classification')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.annotate(
            question_count=models.Count('question')
        ).order_by('-question_count')
        context['not_classified'] = Question.objects.filter(
            tag__isnull=True).count()
        return context
