from django.db.models import Q
from django.db.models import Count


from rest_framework import generics
from rest_framework import authentication, permissions, serializers, status, pagination
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, ListAPIView

from django.shortcuts import render
from account.models import UserAccount
from common.models import Language, Tag, Comment, Good
from common.pagesrializers import LargePagination
from .serializers import ArticleSerializer
from .models import Article

#########################
# 記事投稿
#########################


class ArticleView(APIView):
    serializer_class = ArticleSerializer

    def post(self, request):
        """
        投稿
        JWTトークンからrequest.userでアカウントを取得
        """
        try:
            data = request.data
            language = data["language"]
            title = data["title"]
            tags = data["tag"]
            description = data["description"]
            is_public = data["is_public"]
            account = request.user
            language = Language.objects.get(name=language)
            article = Article(
                username=account,
                language=language,
                title=title,
                description=description,
                is_public=is_public
            )
            article.save()
            for tag in tags:
                for i in tag.values():
                    # 入力されたタグがモデルにない場合は新規作成、ある場合はタグを追加
                    if not Tag.objects.filter(name=i).exists():
                        created_tag = Tag(name=i)
                        created_tag.save()
                        article.tag.add(created_tag)
                    else:
                        get_tag = Tag.objects.get(name=i)
                        article.tag.add(get_tag)

            return Response(
                {'success': '記事投稿に成功しました'},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {'error': '記事投稿時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        """投稿編集"""
        # JWT TokenのUserIdと投稿主のIDが同じであれば編集可能
        try:
            data = request.data
            user_id = data["user_id"]
            article_id = data["article_id"]
            language = data["language"]
            title = data["title"]
            tags = data["tag"]
            description = data["description"]
            is_public = data["is_public"]
            article = Article.objects.get(id=article_id)

            if str(request.user.id) == str(user_id):
                # if thumbnail:
                #     article.thumbnail = thumbnail
                language = Language.objects.get(name=language)
                article.language = language
                article.title = title
                article.description = description
                article.is_public = is_public
                # 記事についているタグを外す
                article.tag.clear()
                article.save()
                for tag in tags:
                    for i in tag.values():
                        # 入力されたタグがモデルにない場合は新規作成
                        if not Tag.objects.filter(name=i).exists():
                            created_tag = Tag(name=i)
                            created_tag.save()
                            article_add = article.tag.add(created_tag)
                        else:
                            get_tag = Tag.objects.get(name=i)
                            article_add = article.tag.add(get_tag)

                return Response(
                    {'success': '記事編集に成功しました'},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {'error': '違うユーザーです'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except:
            return Response(
                {'error': '記事編集時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """投稿削除"""

        # JWT TokenのUserIdと投稿主のIDが同じであれば削除可能
        try:
            data = request.data
            user_id = data["user_id"]
            article_id = data["article_id"]

            if str(request.user.id) == str(user_id):
                article = Article.objects.get(
                    id=article_id
                )
                article.delete()
                return Response(
                    {'success': '記事削除に成功しました'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {'error': '違うユーザーです'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except:
            return Response(
                {'error': '記事編集時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 記事一覧、記事検索
class ArticleListView(generics.ListAPIView):
    """
    GET
    api/article/article_list/
    api/article/article_list/?tag=
    api/article/article_list/?tag=&lang=
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Article.objects.filter(is_public=True).order_by('-posted_at')
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """
        ?tag=で渡されたキーワードを用いて、記事のタイトルに含まれているものを出力する
        """
        queryset = super().get_queryset()
        language = self.request.GET.get('lang')
        keyword = self.request.GET.get('tag')
        # ?lang= でパラメータが渡されている場合
        if language is not None:
            # ?lang= &?tag= 両方で検索している場合
            if keyword is not None:
                queryset = queryset.filter(Q(title__icontains=keyword) | Q(
                    tag__name__icontains=keyword), language__name__icontains=language, is_public=True).order_by('-posted_at')
            # ?lang=のみで検索している場合
            else:
                queryset = queryset.filter(Q(language__name__icontains=language) | Q(
                    tag__name__icontains=language), is_public=True).order_by('-posted_at')
        # ?tag= でのみ検索している場合
        elif keyword is not None:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(tag__name__icontains=keyword) | Q(
                language__name__icontains=keyword), is_public=True).order_by('-posted_at')

        return queryset

# グッド数が多い順記事


class ArticleGoodRankingView(generics.ListAPIView):
    """
    GET
    api/article_good_ranking/
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Article.objects.annotate(Count('good')).filter(
        is_public=True).order_by('-good__count')
    serializer_class = ArticleSerializer
    pagination_class = LargePagination


# 記事一覧、記事検索(ページ表示数多め)
class ArticleListPageLargeView(generics.ListAPIView):
    """
    GET
    api/article_list/
    api/article_list/?tag=
    api/article_list/?tag=&lang=
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Article.objects.filter(is_public=True).order_by('-posted_at')
    serializer_class = ArticleSerializer
    pagination_class = LargePagination

    def get_queryset(self):
        """
        ?tag=で渡されたキーワードを用いて、記事のタイトルに含まれているものを出力する
        """
        queryset = super().get_queryset()
        language = self.request.GET.get('lang')
        keyword = self.request.GET.get('tag')
        # ?lang= でパラメータが渡されている場合
        if language is not None:
            # ?lang= &?tag= 両方で検索している場合
            if keyword is not None:
                queryset = queryset.filter(Q(title__icontains=keyword) | Q(
                    tag__name__icontains=keyword), language__name__icontains=language, is_public=True).order_by('-posted_at')
            # ?lang=のみで検索している場合
            else:
                queryset = queryset.filter(Q(language__name__icontains=language) | Q(
                    tag__name__icontains=language), is_public=True).order_by('-posted_at')
        # ?tag= でのみ検索している場合
        elif keyword is not None:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(tag__name__icontains=keyword) | Q(
                language__name__icontains=keyword), is_public=True).order_by('-posted_at')

        return queryset


class ArticleDetailView(RetrieveAPIView):
    """
    記事詳細画面
    api/article/<int:pk>で記事の詳細を見る
    """
    permission_classes = (permissions.AllowAny, )
    # queryset = Article.objects.filter(is_public=True)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'


#####################
# 記事コメント投稿
#####################
class ArticleCommentAPIView(APIView):
    serializer_class = ArticleSerializer

    def post(self, request):
        try:
            data = request.data
            account = request.user
            comment = data["comment"]
            article_id = data["article_id"]
            create_comment = Comment(username=account, comment=comment)
            article = Article.objects.get(id=article_id)
            create_comment.save()
            article.comment.add(create_comment)
            return Response(
                {'success': "コメント投稿に成功しました"},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {'error': 'コメント投稿に失敗しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ArticleGoodAPIView(APIView):
    #####################
    # 記事グッド
    #####################
    serializer_class = ArticleSerializer

    def post(self, request):
        try:
            data = request.data
            account = request.user
            article_id = data["article_id"]
            if not Good.objects.filter(username=account).exists():
                good = Good(username=account)
                good.save()
            # if Article.objects.filter(id=23, good=good)
            else:
                good = Good.objects.get(username=account)
            article = Article.objects.get(id=article_id)
            # related_nameを指定していない場合
            # if article in good.article_set.all():
            # related_nameをarticleに指定
            # もしすでに記事にグッドされていたら
            if article in good.article.all():
                # グッドを削除する
                article.good.remove(good)
                return Response(
                    {'success': "グッド削除に成功しました"},
                    status=status.HTTP_200_OK
                )
            else:
                # グッドを追加する
                article.good.add(good)
                return Response(
                    {'success': "グッドに成功しました"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'success': "グッドに失敗しました"},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {'error': 'グッドに失敗しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
