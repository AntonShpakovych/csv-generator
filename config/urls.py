from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("schemas/", include("csv_generator.urls", namespace="csv_generator")),
    path("", RedirectView.as_view(pattern_name="csv_generator:schema-list"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
