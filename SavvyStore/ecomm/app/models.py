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
StateChoices = (
    ("Alabama","Alabama"),
    ("Alaska", "Alaska"),
    ("California", "California"),
    ("Colorado", "Colorado"),
    ("Delware", "Delware"),
    ("Florida", "Florida"),
    ("Georgia", "Georgia"),
    ("Indiana", "Indiana"),
    ("Kentucky", "Kentucky"),
    ("Michigan", "Michigan"),
    ("Missisippi", "Missisippi"),
    ("Nevada", "Nevada"),
    ("New Jersey", "New Jersey"),
    ("New York", "New York"),
    ("North California", "North California"),
    ("North Dakota", "North Dakota"),
    ("Ohio", "Ohio"),
    ("Pennsylvania", "Pennsylvania"),
    ("Oregon", "Oregon"),
    ("Texas", "Texas"),
    ("Virginia", "Virginia"),
    ("Washington", "Washington"),
    
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

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=StateChoices,max_length=100)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
        
    @property
    def total_cost(self):
        return self.quantity * self.product.discountPrice
    

