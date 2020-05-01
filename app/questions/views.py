from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from model.model import (
    model,
    tokenizer,
    tags,
)
from model.tooling import predict

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PredictView(APIView):

    def get(self, request, format=None):
        question = request.query_params.get('question', '')
        return Response(predict(model, tokenizer, tags, question))
