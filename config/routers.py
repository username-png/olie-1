from rest_framework import routers

from django.urls import path

from app.users.views import (
    UserViewSet,
)
from app.questions.views import (
    AnswerViewSet,
    TagViewSet,
    PredictView,
)


v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('tags', TagViewSet, basename='tags')
v1_router.register('answers', AnswerViewSet, basename='answers')

v1_patterns = [
    path('predict/', PredictView.as_view()),
]

v1_urls = v1_router.urls + v1_patterns
