from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer , Cart , OrderPlaced , Payment, Wishlist
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import razorpay
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request,'app/about.html',locals())

def contact(request):
    return render(request,'app/contact.html',locals())


class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title= Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product = product) & Q(user = request.user))
        return render(request,"app/productDetail.html",locals())
    
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,"app/customerregistration.html",locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User Registered Successfully!")
        else:
            messages.warning(request,"Error in Registration.")
        return render(request,"app/customerregistration.html",locals())

    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,"app/profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name,address=address,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request,"Sorry! Error in Data")
        return render(request,"app/profile.html",locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,"app/address.html",locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,"app/updateAddress.html",locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.address = form.cleaned_data['address']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


def message(request):
    return render(request,'app/message.html',locals())

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for i in cart:
        amount += (i.product.discountPrice * i.quantity)
    amount = round(amount,2)
    totalamount = amount + 10
    return render(request, 'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        amount = 0
        for i in cart_items:
            amount += (i.product.discountPrice * i.quantity)
        amount = round(amount,2)
        totalamount = amount + 10
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount" : razoramount, "currency" : "INR", "receipt" : "order_receiptid_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        {'id': 'order_O4pQr0KGxfXa8r', 'entity': 'order', 'amount': 13944, 'amount_paid': 0, 'amount_due': 13944, 'currency': 'INR', 'receipt': 'order_receiptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1714478965}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status,
            )
            payment.save()
        return render(request,'app/checkout.html',locals())


def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    print("payment done : oid = ",order_id, "pid = ",payment_id, "cid = ",cust_id)
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user = user, customer=customer, product = c.product, quantity = c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")

def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    order_placed = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for i in cart:
            amount += (i.product.discountPrice * i.quantity)
        amount = round(amount,2)
        totalamount = amount + 10
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

   
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for i in cart:
            amount += (i.product.discountPrice * i.quantity)
        amount = round(amount,2)
        totalamount = amount + 10
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
  
     
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for i in cart:
            amount += (i.product.discountPrice * i.quantity)
        amount = round(amount,2)
        totalamount = amount + 10
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
    
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html',locals())


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product= Product.objects.get(id = prod_id)
        user = request.user
        Wishlist(user = user, product = product).save()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)
   
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product= Product.objects.get(id = prod_id)
        user = request.user
        Wishlist.objects.filter(user = user, product = product).delete()
        data={
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)