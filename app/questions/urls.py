from django.urls import path

from .views import (
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
        name='questions_predict',
    ),
]
