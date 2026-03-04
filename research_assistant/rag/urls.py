

from django.urls import path
from .views import AskQuestion,health


urlpatterns = [
    path("ask/", AskQuestion.as_view(), name="ask-question"),
    path("health/",health.as_view(),name="check-health")
]