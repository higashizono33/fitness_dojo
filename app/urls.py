from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/group', CreateGroupView.as_view(), name='create_group'),
    path('group/<int:pk>', GroupView.as_view(), name='group'),
    path('activity/group/<int:pk>', ActivityView.as_view(), name='activity'),
    path('request/group/<int:pk>', request_group, name='request'),
    path('request/confirm', RequestView.as_view(), name='request_confirm'),
    path('accept/request/<int:pk>', accept_request, name='accept_request'),
    path('reject/request/<int:pk>', reject_request, name='reject_request'),
    path('profile/user/<int:pk>', ProfileView.as_view(), name='profile'),
    path('reset/password/user/<int:pk>', reset_password, name='reset_password'),
]