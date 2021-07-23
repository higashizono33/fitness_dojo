from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from crispy_forms.bootstrap import PrependedText

User = get_user_model()

class CustomUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50, required=True)
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop("autofocus", None)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout(
            PrependedText('username', '<i class="fas fa-user py-1"></i>', placeholder="username"),
            PrependedText('email', '<i class="fas fa-envelope-square py-1"></i>', placeholder="email"),
            PrependedText('password1', '<i class="fas fa-key py-1"></i>', placeholder="password"),
            PrependedText('password2', '<i class="fas fa-key py-1"></i>', placeholder="password confirmation"),
            ButtonHolder(
                Submit('submit', 'Sign In')
            ),
        )
        helper.form_show_labels = False

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(CustomUserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        helper = self.helper = FormHelper()
        layout = helper.layout = Layout(
            PrependedText('username', '<i class="fas fa-envelope-square py-1"></i>', placeholder="email/username"),
            PrependedText('password', '<i class="fas fa-key py-1"></i>', placeholder="password"),
            ButtonHolder(
                Submit('submit', 'Log In')
            ),
        )
        helper.form_show_labels = False