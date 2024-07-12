from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import TodoSerializer
from .models import Todo
from .permessions import TodoPermesion
from backend.pagination import BasePaginator
from backend.utils import updateRequest , MongoObjectIdMixin

class TodoViewset(MongoObjectIdMixin,ModelViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [TodoPermesion]
    pagination_class = BasePaginator
    lookup_field = '_id'
    lookup_url_kwarg = 'pk'

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).filter(user_id=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        updateRequest(request,{"user":request.user.pk})
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        updateRequest(request,{"user":request.user.pk})
        return super().update(request, *args, **kwargs)
    
    