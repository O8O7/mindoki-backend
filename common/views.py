from django.db.models import Q
from django.db.models import Count


from rest_framework import generics
from rest_framework import authentication, permissions, serializers, status, pagination
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, ListAPIView

from .serializers import LanguageSerializer, GoodSerializer, TagSerializer, CommentSerializer
from .models import Language, Good, Tag, Comment
from .pagesrializers import MaxPagination, LargePagination


class LanguageListView(ListAPIView):
    """
    プログラミング言語、カテゴリー一覧と、
    プログラミング言語でfilterをかけて、言語とカテゴリーを出力する
    GET
    api/common/language_list/
    api/common/language_list/?lang=
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Language.objects.all().order_by("id")
    serializer_class = LanguageSerializer
    pagination_class = MaxPagination

    def get_queryset(self):
        """
        ?lang=で渡された言語を使ってフィルターをかける
        """
        queryset = super().get_queryset()
        keyword = self.request.GET.get('lang')
        if keyword is not None:
            queryset = queryset.filter(name=keyword)
        return queryset


#####################
# コメントグッド
#####################
class CommentGoodAPIView(APIView):
    serializer_class = CommentSerializer

    def post(self, request):
        try:
            data = request.data
            account = request.user
            comment_id = data["comment_id"]
            if not Good.objects.filter(username=account).exists():
                good = Good(username=account)
                good.save()
            else:
                good = Good.objects.get(username=account)
            comment = Comment.objects.get(id=comment_id)
            # もしすでに記事にグッドされていたら
            if comment in good.comment.all():
                # グッドを削除する
                comment.good.remove(good)
                return Response(
                    {'success': "グッド削除に成功しました"},
                    status=status.HTTP_200_OK
                )
            else:
                # グッドを追加する
                comment.good.add(good)
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


class GoodListRetrieve(RetrieveAPIView):
    serializer_class = GoodSerializer
    queryset = Good.objects.all()
    pagination_class = LargePagination


class TagListView(ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.order_by('?')
    serializer_class = TagSerializer
    # pagination_class = LargePagination
    pagination_class = MaxPagination
