from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import UserRetrieve, UserRandom, UserProfileRetrieve, FriendViewSet


# 追加
router = DefaultRouter()
router.register('random', UserRandom)
router.register('friends', FriendViewSet, 'friend')

urlpatterns = [
    path('', include(router.urls)),
    path('user/<uuid:pk>/', UserRetrieve.as_view()),
    path('profile/<uuid:pk>/', UserProfileRetrieve.as_view()),
]
