from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import LoginForm
from django.contrib import auth, messages

# Create your views here.
class LoginView(TemplateView):
    template_name = "login.html"
    form_class = LoginForm

    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        remember_me = form.cleaned_data.get('rememberMe')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        if user is not None:
            if remember_me is True:
                self.request.session.set_expiry(1209600)  # 2 weeks
            else:
                self.request.session.set_expiry(0)  # Until browser closes
            
            return redirect(reverse('accounts:home'))
        
        return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return redirect('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['title'] = "Login"
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

# class RegisterView(TemplateView):
#     template_name = "register.html"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = "Register"
#         return context

class LogoutView(TemplateView):
    """Logout View :)"""
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('accounts:login')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('accounts:login'))
        return super().get(request, *args, **kwargs)