from django.forms import ModelForm
from .models import Event, Group

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