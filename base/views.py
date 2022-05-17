from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Event
from .forms import PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('events')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('events')
        return super(RegisterPage, self).get(*args, **kwargs)


class EventList(LoginRequiredMixin, ListView):
    model = Event
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = context['events'].filter(user=self.request.user)
        context['count'] = context['events'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['events'] = context['events'].filter(
                competitor_name__contains=search_input) | context['events'].filter(
                division__contains=search_input) | context['events'].filter(
                event_name__contains=search_input)

        context['search_input'] = search_input

        return context


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'base/event.html'


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['competitor_name', 'event_name', 'division', 'ring', 'competitors', 'results', 'complete']
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['competitor_name', 'event_name', 'division', 'ring', 'competitors', 'results', 'complete']
    success_url = reverse_lazy('events')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('events')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class EventReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_event_order(positionList)

        return redirect(reverse_lazy('events'))
