from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Question

admin.site.register(Question, MarkdownxModelAdmin)
