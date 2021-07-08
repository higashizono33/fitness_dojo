from .forms import CustomUserCreateForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

User = get_user_model()

class IndexView(TemplateView):
    template_name = 'index.html'

class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        # email = self.request.POST['email']
        # password = self.request.POST['password1']
        # user = authenticate(email=email, password=password)
        login(self.request, user, backend='accounts.backend.EmailOrUsernameModelBackend')
        return redirect(self.success_url)