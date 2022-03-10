from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserAccount
from article.models import Article
from portfolio.models import Portfolio
from friendship.models import FriendshipRequest, Friend, Follow

from portfolio.serializers import PortfolioSerializer
from article.serializers import ArticleSerializer
# from question.serializers import QuestionSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'email', 'image',
                  'introduction')


class UserArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'image')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'image',
                  'introduction', 'following', 'followers')


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name')


class FriendSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField()
    from_user = serializers.StringRelatedField()

    class Meta:
        model = Friend
        fields = ('id', 'to_user', 'from_user', 'created')


class FriendshipRequestSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField()
    from_user = serializers.StringRelatedField()

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user', 'to_user', 'message',
                  'created', 'rejected', 'viewed')
        extra_kwargs = {
            'from_user': {'read_only': True},
            'created': {'read_only': True},
            'rejected': {'read_only': True},
            'viewed': {'read_only': True},
        }


class FriendshipRequestResponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = FriendshipRequest
        fields = ('id',)


class UserSecretProfileSerializer(serializers.ModelSerializer):
    """
    他のユーザーから見るプロフィール
    isPublic=Trueのみを表示
    """
    portfolio = serializers.SerializerMethodField('get_portfolio')
    article = serializers.SerializerMethodField('get_article')

    def get_portfolio(self, useraccount):
        portfolio_queryset = Portfolio.objects.filter(
            is_public=True, username=useraccount)
        serializer = PortfolioSerializer(
            instance=portfolio_queryset, many=True, read_only=True)
        return serializer.data

    def get_article(self, useraccount):
        article_queryset = Article.objects.filter(
            is_public=True, username=useraccount)
        serializer = ArticleSerializer(
            instance=article_queryset, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = UserAccount
        fields = ['id', 'name', 'image', 'introduction',
                  'article', 'portfolio', 'following', 'followers']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    自分のプロフィール
    isPublic=False, True両方ともを表示
    """
    portfolio = PortfolioSerializer(many=True)
    article = ArticleSerializer(many=True)
    # portfolio = serializers.StringRelatedField()
    # article = serializers.StringRelatedField()

    class Meta:
        model = UserAccount
        fields = ['id', 'name', 'image',
                  'introduction', 'article', 'portfolio', 'following', 'followers']
