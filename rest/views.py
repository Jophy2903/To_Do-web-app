from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.models import Task, TaskGroup, Contact, SharedTask
from .serializers import TaskSerializer, TaskGroupSerializer, ContactSerializer, SharedTaskSerializer


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskGroupList(request):
    groups = TaskGroup.objects.all()
    serializer = TaskGroupSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def contactList(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def sharedTaskList(request):
    sharedTasks = SharedTask.objects.all()
    serializer = SharedTaskSerializer(sharedTasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createTask(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response()


@api_view(['POST'])
def createTaskGroup(request):
    serializer = TaskGroupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def createContact(request):
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def createSharedTask(request):
    serializer = SharedTaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
