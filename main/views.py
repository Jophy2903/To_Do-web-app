from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task, TaskGroup, Contact, SharedTask


class TodoLoginView(LoginView):
    template_name = 'main/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class TodoRegisterView(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(TodoRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(TodoRegisterView, self).get(*args, **kwargs)


class TasksView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['pendingTasks'] = context['tasks'].filter(task_status='PENDING')
        context['count'] = context['pendingTasks'].count()
        context['completedTasks'] = context['tasks'].filter(task_status='COMPLETE')
        context['completedCount'] = context['completedTasks'].count()

        context['sharedTasks'] = Task.objects.filter(
            id__in=SharedTask.objects.filter(shared_user_id=self.request.user.id)
                .values_list('task_id', flat=True)).filter(task_status='PENDING')
        context['sharedCount'] = context['sharedTasks'].count()
        return context


class TaskGroupsView(LoginRequiredMixin, ListView):
    model = TaskGroup
    context_object_name = 'groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = context['groups'].filter(user=self.request.user)
        context['count'] = context['groups'].count()
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['group', 'task_name', 'task_description']
    template_name = 'main/create-task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)

    # filtered taskgroup to display only logged-in user task group
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['group'].queryset = TaskGroup.objects.filter(user=self.request.user)
        return form


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task_status']
    template_name = 'main/task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdateView, self).form_valid(form)


class TaskGroupCreateView(LoginRequiredMixin, CreateView):
    model = TaskGroup
    fields = ['group_name', 'group_description']
    template_name = 'main/create-group.html'
    success_url = reverse_lazy('groups')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskGroupCreateView, self).form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'main/delete-task.html'
    success_url = reverse_lazy('tasks')


class TaskGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskGroup
    context_object_name = 'group'
    template_name = 'main/delete-group.html'
    success_url = reverse_lazy('groups')


class ContactsView(LoginRequiredMixin, ListView):
    model = Contact
    context_object_name = 'contacts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = context['contacts'].filter(user=self.request.user)
        context['count'] = context['contacts'].count()
        return context


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['contact_user']
    template_name = 'main/add-contact.html'
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContactCreateView, self).form_valid(form)

    # excluded current user
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['contact_user'].queryset = User.objects.exclude(id=self.request.user.id)
        return form


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    context_object_name = 'contact'
    template_name = 'main/delete-contact.html'
    success_url = reverse_lazy('contacts')


class SharedTaskCreateView(LoginRequiredMixin, CreateView):
    model = SharedTask
    fields = ['task', 'shared_user']
    template_name = 'main/share-task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        # Set the current user as the user who shared the task
        form.instance.user = self.request.user

        # Get the selected shared user from the form
        shared_user = form.cleaned_data['shared_user']

        # Set the shared user in the form instance
        form.instance.shared_user = shared_user

        # Call the parent method to save the form instance
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['task'].queryset = Task.objects.filter(user=self.request.user)
        form.fields['shared_user'].queryset = Contact.objects.filter(user=self.request.user)
        return form

