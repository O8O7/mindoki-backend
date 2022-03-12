from django.db import models
from account.models import UserAccount

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from common.models import Language, Tag, Comment, Good

import uuid


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="article")
    language = models.ForeignKey(
        Language, on_delete=models.PROTECT, related_name="article")
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    comment = models.ManyToManyField(Comment, verbose_name='コメント', blank=True)
    good = models.ManyToManyField(
        Good, verbose_name='グッド', blank=True, related_name="article")
    title = models.CharField("タイトル", max_length=64)
    description = MarkdownxField()
    edited_at = models.DateTimeField("編集日", auto_now=True)
    posted_at = models.DateTimeField("投稿日", auto_now_add=True)

    is_public = models.BooleanField("公開する", default=False)

    # class Meta:
    #     ordering = ['-posted_at']

    def __str__(self):
        return self.title

    # markdownをHTML化する 参考:https://selfs-ryo.com/detail/nuxt_django_blog_1
    def convert_markdown_to_html(self):
        return markdownify(self.description)
