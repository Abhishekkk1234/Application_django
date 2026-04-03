from django.db import models
from django.contrib.auth.models import User

class UserFormData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    file = models.FileField(upload_to='uploads/')


