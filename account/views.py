from django.contrib.auth import get_user_model

from rest_framework import permissions, serializers, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView

from .serializers import UserSerializer, UserListSerializer, FriendSerializer, FriendshipRequestSerializer, FriendshipRequestResponseSerializer
from .models import UserAccount
from .serializers import UserProfileSerializer, UserSecretProfileSerializer
from common.pagesrializers import LargePagination

from friendship.models import Friend, Follow, Block, FriendshipRequest, FriendshipManager

from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
User = get_user_model()


# アカウント登録
class RegisterView(APIView):
    # AllowAnyで認証しなくてもAPIに接続できるようになる
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data
            name = data['name']
            email = data['email'].lower()
            password = data['password']

            # ユーザーの存在確認
            if not User.objects.filter(email=email).exists():
                # ユーザーが存在しない場合は作成
                User.objects.create_user(
                    name=name, email=email, password=password)

                return Response(
                    {'success': 'ユーザーの作成に成功しました'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': 'すでに登録されているメールアドレスです'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except:
            return Response(
                {'error': 'アカウント登録時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ユーザー情報取得


class UserView(APIView):
    def get(self, request):
        try:
            user = request.user
            # UserSerializerでjson形式にする
            user = UserSerializer(user, context={"request": request})

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )

        except:
            return Response(
                {'error': 'ユーザーの取得に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserRetrieve(RetrieveAPIView):
    """
    誰でも検索できる
    GET
    api/auth/user/<int:pk>
    """
    permission_classes = (permissions.AllowAny, )
    queryset = UserAccount.objects.all()
    serializer_class = UserListSerializer


class UserProfileRetrieve(RetrieveAPIView):
    """
    誰でも検索できる
    GET
    api/auth/user/<int:pk>
    """
    permission_classes = (permissions.AllowAny, )
    queryset = UserAccount.objects.all()
    serializer_class = UserSecretProfileSerializer
    pagination_class = LargePagination

# ユーザーをランダムで20個取り出す


class UserRandom(ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = UserAccount.objects.order_by('?')[:20]
    serializer_class = UserListSerializer


class FriendViewSet(ModelViewSet):
    serializer_class = UserListSerializer
    lookup_field = 'pk'

    def list(self, request):
        """
        フレンドリストを表示
        # /api/auth/friends/
        Method:GET
        """
        friend_requests = Friend.objects.friends(user=request.user)
        self.queryset = friend_requests
        self.http_method_names = ['get', 'head', 'options', ]
        # self.http_method_names = ['get']
        return Response(UserListSerializer(friend_requests, many=True).data)

    # /api/auth/friends/[pk]でJWTTokenユーザーとフレンド関係があるか確認
    # フレンドであれば[pk]フレンドのユーザーを取得
    def retrieve(self, request, pk=None):
        self.queryset = Friend.objects.friends(user=request.user)
        requested_user = get_object_or_404(User, pk=pk)
        if Friend.objects.are_friends(request.user, requested_user):
            self.http_method_names = ['get', 'head', 'options', ]
            return Response(UserListSerializer(requested_user, many=False).data)
        else:
            return Response(
                {'message': "フレンドの関係が見つかりません"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # detail=Falseはurlにidが含まれないもの
    # /api/auth/friends/requests/
    @ action(detail=False)
    def requests(self, request):
        friend_requests = Friend.objects.unrejected_requests(user=request.user)
        self.queryset = friend_requests
        # print(friend_requests)
        return Response(
            FriendshipRequestSerializer(friend_requests, many=True).data)

    # /api/auth/follower
    # フォローワー一覧

    @action(detail=False)
    def follower(self, request):
        followers = Follow.objects.followers(user=request.user)
        return Response(
            UserListSerializer(followers, many=True).data
        )

    # /api/auth/following
    # フォローしている人一覧
    @action(detail=False)
    def following(self, request):
        following = Follow.objects.following(user=request.user)
        return Response(
            UserListSerializer(following, many=True).data
        )

# friend = Follow.objects.followers(user=account4)
# >>> friend
# [<UserAccount: firesamurai.
# jp@gmail.com>, <UserAccount: yoshi@gmail.com>,
# <UserAccount: sand@sample.com>, <UserAccount: tech@gmail.com>]

    # /api/auth/friends/sent_requests/
    # 送ったフレンドリクエスト
    @ action(detail=False)
    def sent_requests(self, request):
        friend_requests = Friend.objects.sent_requests(user=request.user)
        self.queryset = friend_requests
        return Response(
            FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False)
    def rejected_requests(self, request):
        friend_requests = Friend.objects.rejected_requests(user=request.user)
        self.queryset = friend_requests
        return Response(
            FriendshipRequestSerializer(friend_requests, many=True).data)

    @ action(detail=False,
             serializer_class=FriendshipRequestSerializer,
             methods=['post'])
    def add_friend(self, request, username=None):
        """
        /api/auth/friends/add_friend/ フォームデータ "to_user": "[id]"でフレンドを追加
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = get_object_or_404(
            UserAccount,
            id=serializer.validated_data.get('to_user')
        )

        try:
            friend_obj = Friend.objects.add_friend(
                # The sender
                request.user,
                # The recipient
                to_user,
                # Message (...or empty str)
                message=request.data.get('message', '')
            )
            return Response(
                FriendshipRequestSerializer(friend_obj).data,
                status.HTTP_201_CREATED
            )
        except (AlreadyExistsError, AlreadyFriendsError) as e:
            # エラー分をmessage: エラー分 で返す
            return Response(
                {"message": str(e)},
                status.HTTP_400_BAD_REQUEST
            )

    @ action(detail=False, serializer_class=FriendshipRequestSerializer, methods=['post'])
    def remove_friend(self, request):
        """
        フレンドを削除する
        /api/auth/friends/remove_friend/ 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_user = get_object_or_404(
            UserAccount,
            id=serializer.validated_data.get('to_user')
        )

        if Friend.objects.remove_friend(request.user, to_user):
            message = 'フレンドを削除しました'
            status_code = status.HTTP_204_NO_CONTENT
        else:
            message = 'フレンドではありません'
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(
            {"message": message},
            status=status_code
        )

    @ action(detail=False,
             serializer_class=FriendshipRequestResponseSerializer,
             methods=['post'])
    def accept_request(self, request, id=None):
        """
        フレンド申請を許可する
        /api/auth/friends/remove_friend/
        to_user: [id]
        """
        id = request.data.get('id', None)
        friendship_request = get_object_or_404(
            FriendshipRequest, pk=id)

        if not friendship_request.to_user == request.user:
            return Response(
                {"message": "フレンドリクエストが見つかりませんでした。"},
                status.HTTP_400_BAD_REQUEST
            )

        friendship_request.accept()
        return Response(
            {"message": "フレンドリクエストを許可し、フレンドになりました。"},
            status.HTTP_201_CREATED
        )

    @ action(detail=False,
             serializer_class=FriendshipRequestResponseSerializer,
             methods=['post'])
    def reject_request(self, request, id=None):
        """
        Rejects a friend request
        The request id specified in the URL will be rejected
        """
        id = request.data.get('id', None)
        friendship_request = get_object_or_404(
            FriendshipRequest, pk=id)
        if not friendship_request.to_user == request.user:
            return Response(
                {"message": "Request for current user not found."},
                status.HTTP_400_BAD_REQUEST
            )

        friendship_request.reject()

        return Response(
            {
                "message": "Request rejected, user NOT added to friends."
            },
            status.HTTP_201_CREATED
        )
