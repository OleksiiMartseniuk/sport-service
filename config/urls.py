from django.contrib import admin
from django.urls import path, include

from .yasg import docs_url


api_urlpatterns = [
    # Docs
    path('', include(docs_url)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_urlpatterns)),
]
