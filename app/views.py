from django.views.generic.edit import CreateView
from app.models import Event
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, UpdateView, TemplateView
from .models import Comment, Event, Group, Invitation, Message, Request
from .forms import EventCreateForm, GroupEditForm, ProfileEditForm, ResetPasswordForm, GroupCreateForm
from django.contrib.auth import get_user_model, login
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

# to show numbers in badge at the navbar
def count_not_responded_request(request, logged_user):
    user_groups = Group.objects.filter(creator=logged_user)
    not_responded_req = Request.objects.filter(group__in=user_groups).filter(is_responded=False)
    request.session['count_req'] = not_responded_req.count()
    return 

def count_not_responded_invitation(request, logged_user):
    not_responded_inv = Invitation.objects.filter(invited_who=logged_user).filter(is_responded=False)
    request.session['count_inv'] = not_responded_inv.count()
    return 

class IndexView(TemplateView):
    template_name = 'index.html'

class HomeView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'
    paginate_by = 10
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    
    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        queryset = Event.objects.all().order_by('date','starttime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventCreateForm(user=self.request.user)
        count_not_responded_request(self.request, self.request.user)
        count_not_responded_invitation(self.request, self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = EventCreateForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'form': form,
                'events': self.get_queryset(),
            }
            return render(request, 'home.html', context)

def delete_event(request, event_id):
    event_to_delete = get_object_or_404(Event, pk=event_id)
    if request.user == event_to_delete.group.creator:
        event_to_delete.delete()
    return redirect('home')

def edit_date_event(request, event_id):
    event_to_edit = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        if request.user == event_to_edit.group.creator:
            print(request.POST['date'])
            event_to_edit.date = request.POST['date']
            event_to_edit.save()
            return JsonResponse({'success': f'{event_to_edit.date}'})

def edit_starttime_event(request, event_id):
    event_to_edit = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        if request.user == event_to_edit.group.creator:
            event_to_edit.starttime = request.POST['starttime']
            event_to_edit.save()
            return JsonResponse({'success': f'{event_to_edit.starttime}'})

class CreateGroupView(LoginRequiredMixin, CreateView):
    template_name = 'create_group.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('create_group')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_key'] = settings.GOOGLE_API_KEY
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super(CreateGroupView, self).form_valid(form)

def destroy_group(request, pk):
    destroyed = get_object_or_404(Group, pk=pk)
    if destroyed.creator == request.user:
        destroyed.delete()
    return redirect('create_group')

def exit_group(request, pk):
    exited = get_object_or_404(Group, pk=pk)
    if request.user in exited.member.all():
        exited.member.remove(request.user)
        exited.save()
    return redirect('create_group')

class GroupView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'group.html'
    form_class = GroupEditForm
    context_object_name = 'group'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['non_members'] = User.objects.exclude(join_groups=self.get_object()).exclude(id=self.request.user.id).exclude(is_superuser=True).exclude(invitations__is_responded=False)
        context['api_key'] = settings.GOOGLE_API_KEY
        return context

    def post(self, request, *args, **kwargs):
        group = self.get_object()
        form = GroupEditForm(request.POST, instance=group)
        if form.is_valid():
            update_group = form.save(commit=False)
            update_group.creator = request.user
            update_group.save()
            return redirect('group', group.id)
        else:
            context = {
                'form': form,
                'group': group,
            }
            return render(request, 'group.html', context)

class ActivityView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'activity.html'
    context_object_name = 'events'
    paginate_by = 20
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    
    def get_group(self):
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return group
    
    def get_queryset(self):
        queryset = super(ActivityView, self).get_queryset()
        queryset = Event.objects.filter(group=self.get_group()).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.get_group()
        requests = Request.objects.filter(group=self.get_group()).filter(who_requested=self.request.user)
        if requests.count() > 0:
            context['requested_before'] = True
        if 'event_id' in self.kwargs:
            selected = get_object_or_404(Event, pk=self.kwargs['event_id'])
            context['event'] = selected
            context['messages'] = Message.objects.filter(event=selected)
        else:
            latest = Event.objects.filter(group=self.get_group()).last()
            context['event'] = latest
            context['messages'] = Message.objects.filter(event=latest)
        return context

    def post(self, request, *args, **kwargs):
        if len(request.POST['message']) < 2:
            # print('error')
            # messages.error(request, 'error')
            return JsonResponse({'error': 'Please enter your message at least 2 charactors'})
        else:
            if 'event_id' in self.kwargs:
                new_message = Message.objects.create(
                    event = get_object_or_404(Event, pk=self.kwargs['event_id']),
                    sender = self.request.user,
                    message = self.request.POST['message'],
                )
            else:
                latest = Event.objects.last()
                new_message = Message.objects.create(
                    event = latest,
                    sender = self.request.user,
                    message = self.request.POST['message'],
                )
        if 'event_id' in self.kwargs:
            selected = get_object_or_404(Event, pk=self.kwargs['event_id'])
            event = selected
            messages = Message.objects.filter(event=selected)
        else:
            latest = Event.objects.filter(group=self.get_group()).last()
            event = latest
            messages = Message.objects.filter(event=latest)
        context = {
            'messages': messages,
            # 'event': event,
            # 'group': self.get_group(),
            # 'user': self.request.user,
        }
        html = render_to_string('partial/chat.html', context, request=request)
        return JsonResponse({'html': html})

def comment(request, message_id):
    if request.method == 'POST':
        this_message = get_object_or_404(Message, pk=message_id)
        if len(request.POST['comment']) < 2:
            return JsonResponse({'error': 'Please enter your comment at least 2 charactors'})
        else:
            new_comment = Comment.objects.create(
                message = this_message,
                sender = request.user,
                comment = request.POST['comment'],
            )
        context = {
            'messages': Message.objects.filter(event=this_message.event),
        }
        html = render_to_string('partial/chat.html', context, request=request)
        return JsonResponse({'html': html})
        # return redirect('activity', this_message.event.group.id)

def request_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST' and group.can_request():
        new_request = Request.objects.create(
            who_requested = request.user,
            group = group,
            message = request.POST['message'],
        )
    return redirect('activity', pk)

class RequestView(TemplateView):
    template_name = 'request.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_groups = Group.objects.filter(creator=self.request.user)
        not_responded = Request.objects.filter(group__in=user_groups).filter(is_responded=False)
        if not_responded.count() > 0:
            context['not_responded'] = True
            context['current_req'] = not_responded[0]
        return context

def accept_request(request, pk):
    accept_req = get_object_or_404(Request, pk=pk)
    if accept_req.group.creator == request.user:
        accept_req.is_responded = True
        accept_req.is_accepted = True
        accept_req.save()
        accept_req.group.member.add(accept_req.who_requested)
        count_not_responded_request(request, request.user)
    return redirect('request_confirm')

def reject_request(request, pk):
    reject_req = get_object_or_404(Request, pk=pk)
    reject_req.is_responded = True
    reject_req.save()
    count_not_responded_request(request, request.user)
    return redirect('request_confirm')

def invite_group(request, pk):
    # invited_before = Invitation.objects.filter(group=group).filter(invited_who=invited_user)
    # if request.method == 'POST' and invited_before.count() == 0:
    if request.method == 'POST' and request.POST['user'] != '':
        group = get_object_or_404(Group, pk=pk)
        invited_user = get_object_or_404(User, pk=request.POST['user'])
        new_invitation = Invitation.objects.create(
            group = group,
            invited_who = invited_user,
        )
    return redirect('group', pk)

class InvitationView(TemplateView):
    template_name = 'invitation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        not_responded = Invitation.objects.filter(invited_who=self.request.user).filter(is_responded=False)
        if not_responded.count() > 0:
            context['not_responded'] = True
            context['current_inv'] = not_responded[0]
        context['api_key'] = settings.GOOGLE_API_KEY
        return context

def accept_invitation(request, pk):
    accept_inv = get_object_or_404(Invitation, pk=pk)
    if accept_inv.invited_who == request.user:
        accept_inv.is_responded = True
        accept_inv.is_accepted = True
        accept_inv.save()
        accept_inv.group.member.add(accept_inv.invited_who)
        count_not_responded_invitation(request, request.user)
    return redirect('invitation_confirm')

def reject_invitation(request, pk):
    reject_inv = get_object_or_404(Invitation, pk=pk)
    reject_inv.is_responded = True
    reject_inv.save()
    count_not_responded_invitation(request, request.user)
    return redirect('invitation_confirm')

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile.html'
    form_class = ProfileEditForm
    context_object_name = 'profile'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p_form'] = ResetPasswordForm(self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        update_user = self.get_object()
        form = ProfileEditForm(request.POST, request.FILES, instance=update_user)
        if form.is_valid():
            update_object = form.save(commit=False)
            update_object.save()
            form.save_m2m()
            return redirect('profile', update_user.id)
        else:
            context = {
                'form': form,
                'p_form': ResetPasswordForm(self.get_object()),
                'profile': update_user,
            }
            return render(request, 'profile.html', context)

def reset_password(request, pk):
    update_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ResetPasswordForm(update_user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user.username)
            return redirect('profile', update_user.id)
        else:
            context = {
                'profile': update_user,
                'p_form': form,
                'form': ProfileEditForm(instance=update_user),
            }
            return render(request, 'profile.html', context) 
    return redirect('profile', update_user.id)
