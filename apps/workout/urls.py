from django.urls import path

from . import views


api_urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='categories'),
]
