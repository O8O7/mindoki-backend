from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('メールアドレスは必須です')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("メールアドレス", max_length=64, unique=True)
    name = models.CharField("名前", max_length=32)
    image = models.ImageField(
        upload_to='images', verbose_name='プロフィール画像', default='images/default.png')
    introduction = models.CharField(
        verbose_name="自己紹介", max_length=255, default="自己紹介は現在登録されていません")
    updated_at = models.DateTimeField("更新日", auto_now=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


# class FriendList(models.Model):
#     user = models.OneToOneField(
#         UserAccount, on_delete=models.CASCADE, related_name="user")
#     # user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="user")
#     friends = models.ManyToManyField(
#         UserAccount, related_name="friend", blank=True)

#     def __str__(self):
#         return self.user.name

#     def add_friend(self, account):
#         if not account in self.friends.all():
#             self.friends.add(account)

    # def remove_friend(self, account):
    #     if account in self.friends.all():
    #         self.friends.remove(account)

    # def unfriend(self, remove):
    #     remover_friends_list = self
    #     remover_friends_list.remove_friend(remove)
    #     friends_list = FriendList.objects.get(user=remove)
    #     friends_list.remove_friend(self.user)

    # def is_mutual_friend(self, friend):
    #     """
    #     Is this a friend
    #     """
    #     if friend in self.friends.all():
    #         return True
    #     return False


# class FriendRequest(models.Model):
#     sender = models.ForeignKey(
#         UserAccount, on_delete=models.CASCADE, related_name="sender")
#     receiver = models.ForeignKey(
#         UserAccount, on_delete=models.CASCADE, related_name="receiver")
#     is_active = models.BooleanField(blank=True, null=False, default=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.sender.name

#     def accept(self):
#         reveiver_friend_list = FriendList.objects.get(user=self.receiver)

#         if receiver_friend_list:
#             receiver_friend_list.add_friend(self.sender)
#             sender_friend_list = FriendList.objects.get(user=self.sender)
#             if sender_friend_list:
#                 sender_friend_list.add_friend(self.receiver)
#                 self.is_active = False
#                 self.save()

#     def decline(self):
#         """
#         Decline a friend request
#         It is “declined” by settings the 'is_active' field to False
#         """
#         self.is_active = False
#         self.save()

#     def cancel(self):
#         """
#         Cancel a friend request
#         It is 'cancelled' by setting the 'is_active' field to False
#         This is only diffrent with respect "declining" through the notification that
#         is generated
#         """
#         self.is_active = False
#         self.save()
