from django.contrib import admin
from django.urls import path, include

from apps.account import urls as account_url

from .yasg import docs_url


api_urlpatterns = [
    # Docs
    path('', include(docs_url)),
]

for app_url in (account_url,):
    api_urlpatterns.extend(getattr(app_url, "api_urlpatterns", []))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
]
