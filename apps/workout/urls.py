from django.urls import path

from . import views


workout_list = views.WorkoutView.as_view({
    'get': 'list',
    'post': 'create',
})
workout_detail = views.WorkoutView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

api_urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('workout/', workout_list, name='workout-list'),
    path('workout/<int:pk>/', workout_detail, name='workout-detail'),
]
