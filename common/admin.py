from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Language, Tag, Good, Comment


admin.site.register(Language)
admin.site.register(Tag)
admin.site.register(Comment, MarkdownxModelAdmin)
admin.site.register(Good)
