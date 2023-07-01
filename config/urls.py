from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.account import urls as account_url
from apps.workout import urls as workout_url
from apps.history import urls as history_url

from .yasg import docs_url


api_urlpatterns = [
    # Docs
    path('', include(docs_url)),
]

for app_url in (
    account_url,
    workout_url,
    history_url,
):
    api_urlpatterns.extend(getattr(app_url, "api_urlpatterns", []))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
