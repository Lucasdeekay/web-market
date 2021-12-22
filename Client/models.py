from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)
    address = models.TextField()
    bio = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to="images/")

    def __str__(self):
        return f"{self.user}"


