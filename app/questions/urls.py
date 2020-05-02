from django.urls import path

from .views import (
    AnswerCreateView,
    ClassificationView,
    PredictDemoView,
)


urlpatterns = [
    path(
        'classification/',
        ClassificationView.as_view(),
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
]
