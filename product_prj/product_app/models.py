import random
from django.db import models

def generate_product_id():
    return random.randint(10**11, (10**12) - 1)


class Product(models.Model):
    p_id = models.BigAutoField(primary_key=True,default=generate_product_id,unique=True,editable=False)  
    p_name = models.CharField(max_length=255)
    p_description = models.TextField()
    p_quantity = models.IntegerField()
    p_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.p_name
