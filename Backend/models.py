from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class chatdb(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField()
    response=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
