from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):

    due_date = serializers.DateTimeField(input_formats=["%Y-%m-%d %H:%M %z"],format='%d %b, %Y %I:%M %p')

    class Meta:
        model = Todo
        fields = ('__all__')