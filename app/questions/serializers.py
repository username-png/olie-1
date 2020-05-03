from rest_framework import serializers

from .models import (
    Answer,
    Question,
    Tag,
)


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'text')


class TagListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'slug', 'name',)


class TagSerializer(serializers.ModelSerializer):

    sample_questions = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'slug', 'name', 'sample_questions')

    def get_sample_questions(self, instance):
        return [
            question.text for question in instance.question_set.all()[:3]
        ]


class AnswerSerializer(serializers.ModelSerializer):

    tag = serializers.CharField()

    class Meta:
        model = Answer
        fields = ('id', 'text', 'tag',)
