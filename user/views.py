from django.urls import reverse_lazy
from django.views import generic

from user.forms import CustomUserCreationForm


class CreateCustomUserView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_signup"] = True

        return context
