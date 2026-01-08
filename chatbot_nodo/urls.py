from django.urls import path
from .views import chatbot_webhook

urlpatterns = [
    path("webhook/", chatbot_webhook, name="chatbot_webhook"),
]
