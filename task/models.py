from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=False)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"title: {self.title}, description: {self.description}, created: {self.created}, datecompleted: {self.datecompleted}, important: {self.important}, user: {self.user.username}"
