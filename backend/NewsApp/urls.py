from django.urls import path
# pyrefly: ignore [missing-import]
from . import views

urlpatterns = [
    path("tech/", views.TechNewsView),
]