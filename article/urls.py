from rest_framework import routers
from django.urls import path

from .views import (
    ArticleView,
    ArticleListView,
    ArticleDetailView,
    ArticleGoodRankingView,
    ArticleListPageLargeView,
    ArticleCommentAPIView,
    ArticleGoodAPIView,
)

urlpatterns = [
    path('', ArticleView.as_view()),
    path('list/', ArticleListView.as_view()),
    path('list_large/', ArticleListPageLargeView.as_view()),
    path('good_ranking/', ArticleGoodRankingView.as_view()),
    path('<uuid:pk>/', ArticleDetailView.as_view()),
    path('comment/', ArticleCommentAPIView.as_view()),
    path('good/', ArticleGoodAPIView.as_view()),
]
