from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'history-workout', views.HistoryWorkoutView)

api_urlpatterns = []

api_urlpatterns += router.urls
