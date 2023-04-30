from django.urls import path, include

from . import views


api_urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
