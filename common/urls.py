from rest_framework import routers
from django.urls import path

from .views import (
    LanguageListView,
    CommentGoodAPIView,
    GoodListRetrieve,
    TagListView,
)

urlpatterns = [
    path('language_list/', LanguageListView.as_view()),
    path('comment/good/', CommentGoodAPIView.as_view()),
    path('good/<int:pk>/', GoodListRetrieve.as_view()),
    path('tag/', TagListView.as_view()),
]
