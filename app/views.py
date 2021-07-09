from app.models import Event
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView
from .models import Event
from .forms import EventCreateForm

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
        form = EventCreateForm(self.request.POST, user=request.user)
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
