import uuid

from django.db import models
from account.models import UserAccount

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from common.models import Language, Tag, Comment, Good
from mysite import settings


class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="portfolio")
    language = models.ForeignKey(
        Language, on_delete=models.PROTECT, related_name="portfolio")
    # blankはDjangoのフォームからの投稿が空かどうかを判定するもの
    # nullはデータベースの中身が空かどうかを判定するものになります
    title = models.CharField("タイトル", max_length=64)
    tag = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)
    comment = models.ManyToManyField(Comment, verbose_name='コメント', blank=True)
    good = models.ManyToManyField(
        Good, verbose_name='グッド', blank=True, related_name="portfolio")
    description = MarkdownxField()
    edited_at = models.DateTimeField("編集日", auto_now=True)
    posted_at = models.DateTimeField("投稿日", auto_now_add=True)

    is_public = models.BooleanField("公開する", default=False)

    def __str__(self):
        return self.title

    # markdownをHTML化する 参考:https://selfs-ryo.com/detail/nuxt_django_blog_1
    def convert_markdown_to_html(self):
        return markdownify(self.description)


class Image(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField(upload_to='images', verbose_name='サムネイル画像',
                              default='images/default.png', null=False, blank=False)

    def __str__(self):
        # return 'http://localhost:8000%s%s' % (settings.MEDIA_URL, str(self.image))
        return '%s%s%s' % (settings.DJANGO_DOMAIN, settings.MEDIA_URL, str(self.image))
