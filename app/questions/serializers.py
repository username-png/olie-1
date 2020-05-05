from django.http import Http404

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
    random_question = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'slug', 'name', 'sample_questions', 'random_question')

    def get_sample_questions(self, instance):
        return [
            question.text for question in instance.question_set.all()[:3]
        ]

    def get_random_question(self, instance):
        return Question.objects.filter(
            tag=instance.id).order_by('?').first().text


class AnswerSerializer(serializers.ModelSerializer):

    tag = serializers.CharField()

    class Meta:
        model = Answer
        fields = ('id', 'text', 'tag',)

    def create(self, validated_data):
        try:
            tag = Tag.objects.get(slug=validated_data['tag'])
        except Tag.DoesNotExist:
            raise Http404
        return Answer.objects.create(text=validated_data['text'], tag=tag)
