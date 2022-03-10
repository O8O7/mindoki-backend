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
from .serializers import QuestionSerializer
from .models import Question


#########################
# Q&A投稿
#########################
class QuestionView(APIView):
    serializer_class = QuestionSerializer

    def post(self, request):
        """
        投稿
        JWTトークンからrequest.userでメールアドレスを取得
        """
        try:
            data = request.data
            language = data["language"]
            tags = data["tag"]
            title = data["title"]

            description = data["description"]
            account = UserAccount.objects.get(email=request.user)
            language = Language.objects.get(name=language)
            question = Question(
                username=account,
                language=language,
                title=title,
                description=description,
            )
            question.save()
            for tag in tags:
                for i in tag.values():
                    # 入力されたタグがモデルにない場合は新規作成、ある場合はタグを追加
                    if not Tag.objects.filter(name=i).exists():
                        created_tag = Tag(name=i)
                        created_tag.save()
                        question.tag.add(created_tag)
                    else:
                        get_tag = Tag.objects.get(name=i)
                        question.tag.add(get_tag)

            return Response(
                {'success': 'Q&A投稿に成功しました'},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {'error': 'Q&A投稿時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        """投稿編集"""
        # JWT TokenのUserIdと投稿主のIDが同じであれば編集可能
        try:
            data = request.data
            user_id = data["user_id"]
            question_id = data["question_id"]
            language = data["language"]
            title = data["title"]
            tags = data["tag"]
            description = data["description"]
            question = Question.objects.get(id=question_id)

            if str(request.user.id) == str(user_id):
                # if thumbnail:
                #     question.thumbnail = thumbnail
                language = Language.objects.get(name=language)
                question.language = language
                question.title = title
                question.description = description
                question.is_public = is_public
                # 記事についているタグを外す
                question.tag.clear()
                question.save()
                for tag in tags:
                    for i in tag.values():
                        # 入力されたタグがモデルにない場合は新規作成
                        if not Tag.objects.filter(name=i).exists():
                            created_tag = Tag(name=i)
                            created_tag.save()
                            question.tag.add(created_tag)
                        else:
                            get_tag = Tag.objects.get(name=i)
                            question.tag.add(get_tag)

                return Response(
                    {'success': 'Q&A編集に成功しました'},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {'error': '違うユーザーです'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except:
            return Response(
                {'error': 'Q&A編集時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """投稿削除"""

        # JWT TokenのUserIdと投稿主のIDが同じであれば削除可能
        try:
            data = request.data
            user_id = data["user_id"]
            question_id = data["question_id"]

            if str(request.user.id) == str(user_id):
                question = Question.objects.get(
                    id=question_id
                )
                article.delete()
                return Response(
                    {'success': 'Q&A削除に成功しました'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {'error': '違うユーザーです'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        except:
            return Response(
                {'error': 'Q&A編集時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# 記事一覧、記事検索


class QuestionListView(ListAPIView):
    """
    GET
    api/question_list/
    api/question_list/?tag=
    api/question_list/?tag=&lang=
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Question.objects.all().order_by('-posted_at')
    serializer_class = QuestionSerializer

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
                    tag__name__icontains=keyword), language__name__icontains=language).order_by('-posted_at')
            # ?lang=のみで検索している場合
            else:
                queryset = queryset.filter(Q(language__name__icontains=language) | Q(
                    tag__name__icontains=language)).order_by('-posted_at')
        # ?tag= でのみ検索している場合
        elif keyword is not None:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(tag__name__icontains=keyword) | Q(
                language__name__icontains=keyword)).order_by('-posted_at')

        return queryset


# 記事一覧、記事検索(ページ数多め)
class QuestionListPageLargeView(generics.ListAPIView):
    """
    GET
    api/question_list/
    api/question_list/?tag=
    api/question_list/?tag=&lang=
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Question.objects.all().order_by('-posted_at')
    serializer_class = QuestionSerializer
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
                    tag__name__icontains=keyword), language__name__icontains=language).order_by('-posted_at')
            # ?lang=のみで検索している場合
            else:
                queryset = queryset.filter(Q(language__name__icontains=language) | Q(
                    tag__name__icontains=language)).order_by('-posted_at')
        # ?tag= でのみ検索している場合
        elif keyword is not None:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(tag__name__icontains=keyword) | Q(
                language__name__icontains=keyword)).order_by('-posted_at')

        return queryset


class QuestionDetailView(RetrieveAPIView):
    """
    記事詳細画面
    api/question/<uuid:pk>で記事の詳細を見る
    """
    permission_classes = (permissions.AllowAny, )
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'pk'


#####################
# Q&Aコメント投稿
#####################
class QuestionCommentAPIView(APIView):
    serializer_class = QuestionSerializer

    def post(self, request):
        try:
            data = request.data
            account = request.user
            comment = data["comment"]
            question_id = data["question_id"]
            create_comment = Comment(username=account, comment=comment)
            question = Question.objects.get(id=question_id)
            create_comment.save()
            question.comment.add(create_comment)
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
# Q&Aグッド
#####################


class QuestionGoodAPIView(APIView):
    serializer_class = QuestionSerializer

    def post(self, request):
        try:
            data = request.data
            account = request.user
            question_id = data["question_id"]
            if not Good.objects.filter(username=account).exists():
                good = Good(username=account)
                good.save()
            else:
                good = Good.objects.get(username=account)
            question = Question.objects.get(id=question_id)
            # もしすでに記事にグッドされていたら
            if question in good.question.all():
                # グッドを削除する
                question.good.remove(good)
                return Response(
                    {'success': "グッド削除に成功しました"},
                    status=status.HTTP_200_OK
                )
            else:
                # グッドを追加する
                question.good.add(good)
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
