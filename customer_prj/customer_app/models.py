import random
from django.db import models

def generate_customer_id():
    return random.randint(10**11, (10**12) - 1)

class Customer(models.Model):
    c_id = models.BigIntegerField(primary_key=True, default=generate_customer_id, unique=True, editable=False)
    c_fname = models.CharField(max_length=100)
    c_lname = models.CharField(max_length=100)
    c_email = models.EmailField(max_length=100)
    c_phone_number = models.CharField(max_length=20)
    c_city = models.CharField(max_length=50)
    c_pincode = models.CharField(max_length=10, default='0000000')
    c_state = models.CharField(max_length=50)
    c_country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.c_id} - {self.c_fname} {self.c_lname}"
