from django.contrib import admin
from .models import Task, TaskGroup, SharedTask, Contact

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskGroup)
admin.site.register(SharedTask)
admin.site.register(Contact)
