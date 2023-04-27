from django.db import models
from django.contrib.auth.models import User


class TaskGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)
    group_description = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=100)
    TASK_STATUS_CHOICES = (('PENDING', 'PENDING'), ('COMPLETE', 'COMPLETE'))
    task_status = models.CharField(max_length=10, choices=TASK_STATUS_CHOICES, default="PENDING")

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ['task_status']


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user')
    contact_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='contact_user')

    def __str__(self):
        return self.contact_user.__str__()


class SharedTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    shared_user = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.shared_user.contact_user} shared task {self.task}"

