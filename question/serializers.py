from rest_framework import serializers

# from account.serializers import UserArticleSerializer
from common.serializers import LanguageSerializer, CommentSerializer
from .models import Question
from account.models import UserAccount


class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'image')


class QuestionSerializer(serializers.ModelSerializer):
    language = LanguageSerializer()
    comment = CommentSerializer(many=True, read_only=True)
    username = UserQuestionSerializer()

    class Meta:
        model = Question
        fields = [
            'id',
            'username',
            'language',
            'tag',
            'title',
            'comment',
            'good',
            'description',
            'posted_at'
        ]
