from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Portfolio, Image

admin.site.register(Portfolio, MarkdownxModelAdmin)
admin.site.register(Image)
