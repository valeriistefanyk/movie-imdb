from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, FormView, CreateView
from django.urls import reverse

from . import forms


User = get_user_model()


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = 'authentication/login.html'

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data['email'])
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.request.GET.get('next', reverse('auth:account'))


class RegisterView(CreateView):
    form_class = forms.RegistrationForm
    template_name = 'authentication/register.html'

    def get_success_url(self) -> str:
        return self.request.GET.get('next', reverse('auth:account'))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('auth:login')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/account.html'
