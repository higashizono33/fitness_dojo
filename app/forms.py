from django import forms
from django.forms import ModelForm
from .models import Event, Group
from accounts.models import Sport
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()

class EventCreateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.logged_user = user
        super(EventCreateForm, self).__init__(*args, **kwargs)
        group_list = []
        groups = Group.objects.filter(creator=self.logged_user)
        for group in groups:
            group_list.append((group.id, group.name))

        self.fields['group'].choices = group_list
    
    class Meta:
        model = Event
        fields = ['title', 'group', 'location', 'date', 'starttime']

class GroupCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['description'].widget.attrs = {'rows': 5}

    class Meta:
        model = Group
        fields = ['name', 'gym', 'limit', 'level', 'description']

class GroupEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroupEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['description'].widget.attrs = {'rows': 5}

    class Meta:
        model = Group
        fields = ['limit', 'level', 'description']

class ProfileEditForm(ModelForm):
    # photo = forms.ImageField(required=False)
    birthday = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    benchpress = forms.IntegerField(required=False)
    sport = forms.ModelMultipleChoiceField(
            queryset=Sport.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['goal'].widget.attrs = {'rows': 5}
        self.helper = FormHelper()
        self.helper.form_show_labels = False 

    class Meta:
        model = User
        fields = ['photo', 'birthday', 'benchpress', 'sport', 'goal']

class ResetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = None
    
    class Meta:
        model = User