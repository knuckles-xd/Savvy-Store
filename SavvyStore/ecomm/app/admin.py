from django.contrib import admin
from . models import Product, Customer, Cart
# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discountPrice','category','productImage']
    search_fields = ['title']
@admin.register(Customer)
class CutomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','address','city','state','zipcode']
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','product','quantity']
