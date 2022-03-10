from rest_framework import serializers

# from account.serializers import UserArticleSerializer, UserCommentSerializer
# from account.serializers import UserCommentSerializer

# from article.serializers import ArticleSerializer
# from portfolio.serializers import PortfolioSerializer
# from question.serializers import QuestionSerializer
from account.models import UserAccount
from .models import (
    Language,
    Good,
    Comment,
    Tag,
)


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    username = UserCommentSerializer()
    # username = serializers.StringRelatedField()
    good = serializers.StringRelatedField(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'comment', 'posted_at', 'good']


class GoodSerializer(serializers.ModelSerializer):
    # article = ArticleSerializer(many=True, read_only=True)
    # portfolio = PortfolioSerializer(many=True, read_only=True)
    # question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Good
        fields = ['username', 'article', 'portfolio', 'question']
