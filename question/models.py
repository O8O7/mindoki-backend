import uuid
from django.db import models
from account.models import UserAccount

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from common.models import Language, Tag, Comment, Good


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="question")
    language = models.ForeignKey(
        Language, on_delete=models.PROTECT, related_name="question", blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    title = models.CharField("タイトル", max_length=64)
    comment = models.ManyToManyField(Comment, verbose_name='コメント', blank=True)
    good = models.ManyToManyField(
        Good, verbose_name='グッド', blank=True, related_name="question")
    description = MarkdownxField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username.name

    def convert_markdown_to_html(self):
        return markdownify(self.description)
