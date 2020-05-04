from django.urls import path
from django.views.generic import RedirectView

from .views import (
    AnswerCreateView,
    ClassificationView,
    ClassificationDetailView,
    ModelSettingsView,
    PredictDemoView,
)


urlpatterns = [
    path(
        'classification/',
        # TODO: update back to `ClassificationView`
        ClassificationDetailView.as_view(),
        name='questions_classification',
    ),
    path(
        'predict/',
        PredictDemoView.as_view(),
        name='questions_prediction',
    ),
    path(
        'answer/',
        AnswerCreateView.as_view(),
        name='questions_answer',
    ),
    path(
        'model/',
        ModelSettingsView.as_view(),
        name='questions_model',
    ),
    path('', RedirectView.as_view(url='/classification/'), name='index'),
]
