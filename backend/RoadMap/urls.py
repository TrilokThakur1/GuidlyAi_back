from django.urls import path

from . import views

urlpatterns = [
    path('plan', views.RoadMapView),
    path("myPlans",views.MyPlans)
]
