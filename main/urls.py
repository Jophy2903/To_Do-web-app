from django.urls import path

from .views import TodoLoginView, TasksView, TaskGroupsView, TaskCreateView, TaskGroupCreateView, TaskUpdateView, TaskDeleteView, TaskGroupDeleteView, TodoRegisterView, ContactsView, ContactCreateView, ContactDeleteView, SharedTaskCreateView
from django.contrib.auth.views import LogoutView


urlpatterns = [

    path('login/', TodoLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', TodoRegisterView.as_view(), name='register'),

    path('groups', TaskGroupsView.as_view(), name='groups'),
    path('create-group', TaskGroupCreateView.as_view(), name='create-group'),
    path('delete-group/<int:pk>', TaskGroupDeleteView.as_view(), name='delete-group'),

    path('', TasksView.as_view(), name='tasks'),
    path('create-task', TaskCreateView.as_view(), name='create-task'),
    path('task/<int:pk>', TaskUpdateView.as_view(), name='update-task'),
    path('delete-task/<int:pk>', TaskDeleteView.as_view(), name='delete-task'),

    path('contacts', ContactsView.as_view(), name='contacts'),
    path('add-contact', ContactCreateView.as_view(), name='add-contact'),
    path('delete-contact/<int:pk>', ContactDeleteView.as_view(), name='delete-contact'),

    path('share-task/', SharedTaskCreateView.as_view(), name='share-task'),

]
