from djongo import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Todo(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    status = models.CharField(choices=(("Done","Done"),("Pending","Pending"),("Canceled","Canceled"),("Active","Active")),max_length=15)
    due_date = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = 'todo_todo'