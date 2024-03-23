from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CategoryChoices=(
    ('NA','New Arrival'),
    ('PR','Pret'),
    ('WS','Western'),
    ('FR','Formals'),
    ('AC','Accessories'),
    ('FT','Footwear'),
    ('FG','Fragrances'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    originalPrice = models.FloatField()
    discountPrice = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    category = models.CharField(choices=CategoryChoices,max_length=2)
    productImage = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
