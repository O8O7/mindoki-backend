from rest_framework import serializers

from common.serializers import CommentSerializer, LanguageSerializer
from .models import Portfolio, Image
from account.models import UserAccount


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']
        # fields = '__all__'


class UserPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'name', 'image')


class PortfolioSerializer(serializers.ModelSerializer):
    # image = serializers.StringRelatedField(many=True, read_only=True)
    image = ImageSerializer(many=True, read_only=True)
    language = LanguageSerializer()
    comment = CommentSerializer(many=True, read_only=True)
    username = UserPortfolioSerializer()
    # good = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            'id',
            'username',
            'language',
            'image',
            'title',
            'tag',
            'description',
            'posted_at',
            'edited_at',
            'is_public',
            'good',
            'comment'
        ]
