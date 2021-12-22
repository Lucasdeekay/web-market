from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


from Product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    time = models.TimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}|{self.product}"
