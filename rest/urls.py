from django.urls import path

from . import views

urlpatterns = [
    path('tasks/', views.taskList, name="tasks"),
    path('groups/', views.taskGroupList, name="groups"),
    path('contacts/', views.contactList, name="contacts"),
    path('shared-tasks/', views.sharedTaskList, name="sharedTasks"),

    path('task/', views.createTask, name="create-task"),
    path('task-group/', views.createTaskGroup, name="create-task-group"),
    path('contact/', views.createContact, name="create-contact"),
    path('shared-task/', views.createSharedTask, name="create-shared-task"),

    path('update-task/<str:pk>', views.updateTask, name="update-task"),
    path('delete-task/<str:pk>', views.deleteTask, name="delete-task"),
]
