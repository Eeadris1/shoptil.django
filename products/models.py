from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=225)
    price = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='No description available')  # You can specify your default description here
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_pic')

    def __str__(self):
        return self.name

