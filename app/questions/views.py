from pathlib import Path

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.views.generic import (
    DetailView,
    TemplateView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)

from model.tooling import predict

from .forms import (
    QuestionForm,
)
from .models import (
    Answer,
    Question,
    Tag,
)
from .serializers import (
    AnswerSerializer,
    TagSerializer,
    TagListSerializer,
)
from .tasks import retrain_model


class TagViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    serializer_classes = {
        'retrieve': TagSerializer,
        'list': TagListSerializer,
    }
    lookup_field = 'slug'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


class AnswerViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class PredictView(APIView):

    def get(self, request, format=None):
        question = request.query_params.get('question', '')

        prediction = predict(question)
        prediction_tag, prediction_accuracy = (
            prediction[0] if prediction else (None, None))
        prediction_answers = []
        if prediction_tag:
            prediction_answers = Answer.objects.filter(
                tag__slug=prediction_tag).values_list('text', flat=True)

        return Response({
            'tag': prediction_tag,
            'accuracy': prediction_accuracy,
            'answers': prediction_answers,
        })


class ClassificationView(UpdateView):
    template_name_suffix = '_update_form'
    form_class = QuestionForm

    def get_object(self):
        return Question.objects.filter(tag__isnull=True).order_by('?').first()

    def get_success_url(self):
        return reverse('questions_classification')


class ClassificationDetailView(DetailView):
    template_name = 'questions/question_update_form.html'

    def get_object(self, queryset=None):
        return Question.objects.filter(tag__isnull=True).order_by('?').first()

    def post(self, request):
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class PredictDemoView(TemplateView):
    template_name = 'questions/predict_demo.html'


class AnswerCreateView(CreateView):
    model = Answer
    fields = ('text', 'tag',)

    def get_success_url(self):
        return reverse('questions_answer')


class ModelSettingsView(TemplateView):
    template_name = 'questions/model_settings.html'

    def post(self, request):
        # ugly temporary state
        self.retrain = bool(int(request.POST.get('retrain', 0)))
        self.retrain_password = str(request.POST.get('password', ''))
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        model_cache_path = Path('model/data')
        model_cache = model_cache_path / 'model.json'
        model_weights_cache = model_cache_path / 'model.h5'
        tokenizer_cache = model_cache_path / 'tokenizer.json'
        tags_cache = model_cache_path / 'tags.json'

        context['model_cache'] = model_cache.is_file()
        context['model_weights_cache'] = model_weights_cache.is_file()
        context['tokenizer_cache'] = tokenizer_cache.is_file()
        context['tags_cache'] = tags_cache.is_file()

        if getattr(self, 'retrain', False) and self.retrain_password == settings.RETRAIN_PASSWORD:
            context['retrain'] = retrain_model.send()

        return context
