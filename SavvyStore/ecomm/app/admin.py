from django.contrib import admin
from . models import Product, Customer, Cart, Payment, OrderPlaced
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
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']
    
