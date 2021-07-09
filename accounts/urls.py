from django.urls import path
from .views import SignUpView, IndexView
from django.contrib.auth import views
from .forms import CustomLoginForm

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    #overwrite auth-views 'login'
    path('login/', views.LoginView.as_view(template_name="registration/login.html", authentication_form=CustomLoginForm), name='login')
]