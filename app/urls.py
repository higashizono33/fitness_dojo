from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('home', HomeView.as_view(), name='home'),
    path('delete/event/<int:event_id>', delete_event, name='delete_event'),
    path('edit/date/event/<int:event_id>', edit_date_event, name='edit_date_event'),
    path('edit/starttime/event/<int:event_id>', edit_starttime_event, name='edit_starttime_event'),
    path('create/group', CreateGroupView.as_view(), name='create_group'),
    path('destroy/group/<int:pk>', destroy_group, name='destroy_group'),
    path('exit/group/<int:pk>', exit_group, name='exit_group'),
    path('group/<int:pk>', GroupView.as_view(), name='group'),
    path('activity/group/<int:pk>', ActivityView.as_view(), name='activity'),
    path('activity/group/<int:pk>/event/<int:event_id>', ActivityView.as_view(), name='filtered_activity'),
    path('comment/<int:message_id>', comment, name='comment'),
    path('request/group/<int:pk>', request_group, name='request'),
    path('request/confirm', RequestView.as_view(), name='request_confirm'),
    path('accept/request/<int:pk>', accept_request, name='accept_request'),
    path('reject/request/<int:pk>', reject_request, name='reject_request'),
    path('invite/group/<int:pk>', invite_group, name='invite'),
    path('invitation/confirm', InvitationView.as_view(), name='invitation_confirm'),
    path('accept/invitation/<int:pk>', accept_invitation, name='accept_invitation'),
    path('reject/invitation/<int:pk>', reject_invitation, name='reject_invitation'),
    path('profile/user/<int:pk>', ProfileView.as_view(), name='profile'),
    path('reset/password/user/<int:pk>', reset_password, name='reset_password'),
]