import uuid
from django.db import models
from account.models import UserAccount

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Language(models.Model):
    name = models.CharField("プログラミング言語名", max_length=32, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('タグ', primary_key=True, unique=True, max_length=20)

    def __str__(self):
        return self.name


class Good(models.Model):
    username = models.OneToOneField(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="user_comment")
    comment = MarkdownxField()
    posted_at = models.DateTimeField(auto_now_add=True)
    good = models.ManyToManyField(
        Good, verbose_name='コメント', blank=True, related_name="comment")

    def __str__(self):
        return self.comment

    def convert_markdown_to_html(self):
        # return markdownify(self.description)
        return markdownify(self.comment)
