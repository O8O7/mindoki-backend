from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('account.urls')),
    path('friendship/', include('friendship.urls')),
    path('api/common/', include('common.urls')),
    path('api/article/', include('article.urls')),
    path('api/question/', include('question.urls')),
    path('api/portfolio/', include('portfolio.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
