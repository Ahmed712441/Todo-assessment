from django.urls import path
from .views import *

urlpatterns = [
    path('',TodoViewset.as_view({"post":"create","get":"list"})),
    path('<str:pk>/',TodoViewset.as_view({"put":"partial_update","get":"retrieve","delete":"destroy"}))
]
