from django.urls import path

from django.conf import settings
from django.conf.urls.static import static  

from . import views

urlpatterns = [
    path('login', views.LoginView),
    path('register', views.RegisterView),
    path("userDetails",views.UserDetails)
]



urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

