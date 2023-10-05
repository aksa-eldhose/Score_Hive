from django.urls import path

from .views import ScoreView

urlpatterns = [path("save/", ScoreView.as_view(), name="addScore")]
