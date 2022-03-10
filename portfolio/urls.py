from rest_framework import routers
from django.urls import path

from .views import (
    PortfolioView,
    PortfolioListView,
    PortfolioDetailView,
    PortfolioGoodRankingView,
    PortfolioListPageLargeView,
    PortfolioCommentAPIView,
    PortfolioGoodAPIView,
)

urlpatterns = [
    path('', PortfolioView.as_view()),
    path('list/', PortfolioListView.as_view()),
    path('list_large/', PortfolioListPageLargeView.as_view()),
    path('good_ranking/', PortfolioGoodRankingView.as_view()),
    path('<uuid:pk>/', PortfolioDetailView.as_view()),
    path('comment/', PortfolioCommentAPIView.as_view()),
    path('good/', PortfolioGoodAPIView.as_view()),
]
