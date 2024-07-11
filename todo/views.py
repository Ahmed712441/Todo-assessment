from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import TodoSerializer
from .models import Todo

# Create your views here.
class TodoViewset(ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    