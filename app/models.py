from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators
from datetime import date

User = get_user_model()

class Group(models.Model):
    LEVEL_CHOICES = [
        ('B', 'beginner'),
        ('I', 'intermediate'),
        ('A', 'advanced'),
    ]
    creator = models.ForeignKey(User, related_name='own_groups', on_delete=models.CASCADE)
    member = models.ManyToManyField(User, related_name='join_groups')
    name = models.CharField(max_length=100, null=False, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    #limit of members
    limit = models.IntegerField(validators=[validators.MinValueValidator(1, 'Please enter more than 1')])
    gym = models.CharField(max_length=100)
    description = models.TextField(null=True)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def can_request(self):
        if self.member.count() < self.limit:
            return True
        else:
            return False

class Request(models.Model):
    who_requested = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='requests', on_delete=models.CASCADE)
    message = models.TextField(null=True)
    is_responded = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'User#{self.who_requested.id} - {self.group.name}'

class Invitation(models.Model):
    group = models.ForeignKey(Group, related_name='invitations', on_delete=models.CASCADE)
    invited_who = models.ForeignKey(User, related_name='invitations', on_delete=models.CASCADE)
    is_responded = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.group.name} - User#{self.invited_who.id}'

class Event(models.Model):
    group = models.ForeignKey(Group, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, validators=[validators.MinLengthValidator(2, 'Please enter at least 2 charactors')])
    location = models.CharField(max_length=100, null=False)
    date = models.DateField(null=False)
    starttime = models.TimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - Group#{self.group.id}'

    @property
    def is_past(self):
        return date.today() > self.date

class Message(models.Model):
    event = models.ForeignKey(Event, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.id} - User#{self.sender.id}'

class Comment(models.Model):
    message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.id} - User#{self.sender.id}'