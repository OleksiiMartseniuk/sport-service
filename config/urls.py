from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.account import urls as account_url

from .yasg import docs_url


api_urlpatterns = [
    # Docs
    path('', include(docs_url)),
    # Auth JWT
    path('auth/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'auth/jwt/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
]

for app_url in (account_url,):
    api_urlpatterns.extend(getattr(app_url, "api_urlpatterns", []))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
]
