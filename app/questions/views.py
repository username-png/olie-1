from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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
