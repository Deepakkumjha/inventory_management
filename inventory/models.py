from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=100)
    desc=models.TextField(max_length=1000)
    total_quantity=models.PositiveIntegerField()
    low_quantity_flag=models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class BorrowedProduct(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    worker=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField()
    borrowed_data=models.DateField(auto_now_add=True)
    due_date=models.DateField()

    def __str__(self) -> str:
        return self.worker.username
