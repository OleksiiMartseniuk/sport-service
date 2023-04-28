from django.urls import path

from . import views


api_urlpatterns = [
    path(
        'profile/create_user/',
        views.CreateUserView.as_view(),
        name='create_user',
    ),
]
