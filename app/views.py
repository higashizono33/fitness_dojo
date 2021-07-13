from django.views.generic.edit import CreateView
from app.models import Event
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, UpdateView, TemplateView
from .models import Event, Group, Request
from .forms import EventCreateForm, GroupEditForm, ProfileEditForm, ResetPasswordForm, GroupCreateForm
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.db.models import Q

User = get_user_model()

class HomeView(ListView):
    model = Event
    template_name = 'home.html'
    context_object_name = 'events'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super(HomeView, self).get_queryset()
        queryset = Event.objects.all().order_by('created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventCreateForm(user=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = EventCreateForm(request.POST, user=request.user)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'form': form,
                'events': self.get_queryset(),
            }
            return render(request, 'home.html', context)
            # ctx = {}
            # ctx.update(csrf(request))
            # form_html = render_crispy_form(form, context=ctx)
            # return JsonResponse({'success': False, 'form_html': form_html})


class CreateGroupView(CreateView):
    template_name = 'create_group.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('create_group')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super(CreateGroupView, self).form_valid(form)

class GroupView(UpdateView):
    model = Group
    template_name = 'group.html'
    form_class = GroupEditForm
    context_object_name = 'group'

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

class ActivityView(ListView):
    model = Event
    template_name = 'activity.html'
    context_object_name = 'events'
    paginate_by = 20
    
    def get_group(self):
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return group
    
    def get_queryset(self):
        queryset = super(ActivityView, self).get_queryset()
        queryset = Event.objects.filter(group=self.get_group()).order_by('created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.get_group()
        requests = Request.objects.filter(group=self.get_group()).filter(who_requested=self.request.user)
        if requests.count() > 0:
            context['requested_before'] = True
        return context

def request_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if group.can_request():
        new_request = Request.objects.create(
            who_requested = request.user,
            group = group,
        )
        return redirect('activity', pk)
    else:
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
    else:
        pass
    return redirect('request_confirm')

def reject_request(request, pk):
    reject_req = get_object_or_404(Request, pk=pk)
    reject_req.is_responded = True
    reject_req.save()
    return redirect('request_confirm')

class ProfileView(UpdateView):
    model = User
    template_name = 'profile.html'
    form_class = ProfileEditForm
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p_form'] = ResetPasswordForm(self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        update_user = self.get_object()
        form = ProfileEditForm(request.POST, instance=update_user)
        if form.is_valid():
            print('success')
            update_object = form.save(commit=False)
            update_object.save()
            form.save_m2m()
            return redirect('profile', update_user.id)
        else:
            print('error')
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
            update_session_auth_hash(request, user)
            print('success!!')
            return redirect('profile', update_user.id)
        else:
            print('error')
            context = {
                'profile': update_user,
                'p_form': form,
                'form': ProfileEditForm(instance=update_user),
            }
        return render(request, 'profile.html', context) 
    return redirect('profile', update_user.id)
