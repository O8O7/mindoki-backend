from rest_framework import serializers
# from account.serializers import UserArticleSerializer
from common.serializers import LanguageSerializer, CommentSerializer
from .models import Article
from account.models import UserAccount


class UserArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'image')


class ArticleSerializer(serializers.ModelSerializer):
    username = UserArticleSerializer()
    language = LanguageSerializer()
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'username', 'language', 'title', 'tag', 'description',
                  'edited_at', 'posted_at', 'is_public', 'comment', 'good']
