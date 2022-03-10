from django.db.models import Q
from django.db.models import Count


from rest_framework import generics
from rest_framework import authentication, permissions, serializers, status, pagination
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, ListAPIView

from account.models import UserAccount
from common.models import Language, Tag, Comment, Good
from common.pagesrializers import LargePagination

from .serializers import PortfolioSerializer
from .models import Portfolio
from portfolio.models import Image


#########################
# ポートフォリオ投稿
#########################
class PortfolioView(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    serializer_class = PortfolioSerializer

    def post(self, request):
        """
        ポートフォリオ投稿
        JWTトークンからrequest.userでメールアドレスを取得
        """
        try:
            data = request.data
            print(data)
            tags = data.getlist("tag")
            images = request.FILES.getlist('images')
            language = data["language"]
            title = data["title"]
            description = data["description"]
            is_public = data["is_public"]
            account = UserAccount.objects.get(email=request.user)
            language = Language.objects.get(name=language)

            portfolio = Portfolio(
                username=account,
                language=language,
                title=title,
                description=description,
                is_public=is_public
            )
            portfolio.save()
            print(portfolio)
            if tags:
                for i in tags:
                    # 入力されたタグがモデルにない場合は新規作成、ある場合はタグを追加
                    if not Tag.objects.filter(name=i).exists():
                        created_tag = Tag(name=i)
                        created_tag.save()
                        portfolio.tag.add(created_tag)
                    else:
                        get_tag = Tag.objects.get(name=i)
                        portfolio.tag.add(get_tag)

            if images:
                for image in images:
                    created_image = Image(portfolio=portfolio, image=image)
                    created_image.save()
            else:
                return Response(
                    {'error': '画像は1枚以上投稿してください'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {'success': 'ポートフォリオ投稿に成功しました'},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {'error': 'ポートフォリオ投稿時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """投稿削除"""

        # JWT TokenのUserIdと投稿主のIDが同じであれば削除可能
        try:
            data = request.data
            user_id = data["user_id"]
            portfolio_id = data["portfolio_id"]

            if str(request.user.id) == str(user_id):
                portfolio = Portfolio.objects.get(
                    id=portfolio_id
                )
                portfolio.delete()
                return Response(
                    {'success': 'ポートフォリオ削除に成功しました'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {'error': '違うユーザーです'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except:
            return Response(
                {'error': 'ポートフォリオ編集時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ポートフォリオ一覧、ポートフォリオ検索


class PortfolioListView(generics.ListAPIView):
    """
    GET
    api/portfolio/portfolio_list/
    api/portfolio/portfolio_list/?tag=
    api/portfolio/portfolio_list/?tag=&lang=
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Portfolio.objects.filter(is_public=True).order_by('-posted_at')
    serializer_class = PortfolioSerializer

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

# ポートフォリオ一覧、ポートフォリオ検索(ページ表示数多め)


class PortfolioListPageLargeView(generics.ListAPIView):
    """
    GET
    api/portfolio/portfolio_list/
    api/portfolio/portfolio_list/?tag=
    api/portfolio/portfolio_list/?tag=&lang=
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Portfolio.objects.filter(is_public=True).order_by('-posted_at')
    serializer_class = PortfolioSerializer
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


class PortfolioDetailView(RetrieveAPIView):
    """
    記事詳細画面
    api/portfolio/<int:pk>で記事の詳細を見る
    """
    permission_classes = (permissions.AllowAny, )
    # queryset = Portfolio.objects.filter(is_public=True)
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    lookup_field = 'pk'


# グッド数が多い順ポートフォリオ
class PortfolioGoodRankingView(generics.ListAPIView):
    """
    GET
    api/portfolio_good_ranking/
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Portfolio.objects.annotate(Count('good')).filter(
        is_public=True).order_by('-good__count')
    serializer_class = PortfolioSerializer
    pagination_class = LargePagination


#####################
# ポートフォリオコメント投稿
#####################
class PortfolioCommentAPIView(APIView):
    serializer_class = PortfolioSerializer

    def post(self, request):
        try:
            data = request.data
            account = request.user
            comment = data["comment"]
            portfolio_id = data["portfolio_id"]
            create_comment = Comment(username=account, comment=comment)
            portfolio = Portfolio.objects.get(id=portfolio_id)
            create_comment.save()
            portfolio.comment.add(create_comment)
            return Response(
                {'success': "コメント投稿に成功しました"},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {'error': 'コメント投稿に失敗しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

#####################
# ポートフォリオグッド
#####################


class PortfolioGoodAPIView(APIView):
    serializer_class = PortfolioSerializer

    def post(self, request):
        try:
            data = request.data
            account = request.user
            portfolio_id = data["portfolio_id"]
            if not Good.objects.filter(username=account).exists():
                good = Good(username=account)
                good.save()
            else:
                good = Good.objects.get(username=account)
            portfolio = Portfolio.objects.get(id=portfolio_id)
            # もしすでに記事にグッドされていたら
            if portfolio in good.portfolio.all():
                # グッドを削除する
                portfolio.good.remove(good)
                return Response(
                    {'success': "グッド削除に成功しました"},
                    status=status.HTTP_200_OK
                )
            else:
                # グッドを追加する
                portfolio.good.add(good)
                return Response(
                    {'success': "グッドに成功しました"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'success': "グッドに失敗しました"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        except:
            return Response(
                {'error': 'グッドに失敗しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
