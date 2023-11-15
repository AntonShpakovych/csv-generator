from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from user.views import CreateCustomUserView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", CreateCustomUserView.as_view(), name="signup"),
]

app_name = "user"
