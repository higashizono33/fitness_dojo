from django.contrib import admin
from .models import Group, Request, Invitation, Event, Message, Comment

class GroupAdmin(admin.ModelAdmin):
    pass
class RequestAdmin(admin.ModelAdmin):
    pass
class InvitationAdmin(admin.ModelAdmin):
    pass
class EventAdmin(admin.ModelAdmin):
    pass
class MessageAdmin(admin.ModelAdmin):
    pass
class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)