from rest_framework import routers
from django.urls import path

from .views import (
    QuestionView,
    QuestionListView,
    QuestionDetailView,
    QuestionListPageLargeView,
    QuestionCommentAPIView,
    QuestionGoodAPIView,
)

urlpatterns = [
    path('', QuestionView.as_view()),
    path('list/', QuestionListView.as_view()),
    path('list_large/', QuestionListPageLargeView.as_view()),
    path('<uuid:pk>/', QuestionDetailView.as_view()),
    path('comment/', QuestionCommentAPIView.as_view()),
    path('good/', QuestionGoodAPIView.as_view()),
]
