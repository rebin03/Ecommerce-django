from django.shortcuts import render, redirect
from django.views.generic import View
from store.forms import SignUpForm, LoginForm, OrderForm
from store.models import BasketItem, Order, OrderItem, Product, Size, User, WishlistItem
from django.core.mail import send_mail
from twilio.rest import Client
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import os
from decouple import config
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

RZP_KEY_ID = config('RZP_KEY_ID')
RZP_KEY_SECRET = config('RZP_KEY_SECRET')

# Create your views here.

def send_otp_phone(otp):
    
    account_sid = config('ACCOUNT_SID')
    auth_token = config('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_= config('TWILIO_FROM_NUMBER'),
        body=otp,
        to= config('TO_NUMBER')
    )
    print(message.sid)

def send_otp_email(user):
    
    user.generate_otp()
    send_otp_phone(user.otp)
    subject = 'Verify your email'
    message = f'OTP for account verification is {user.otp}'
    from_email = 'iamrbn03@gmail.com'
    to_email = [user.email]
    
    send_mail(subject, message, from_email, to_email)


class SignUpView(View):
    
    template_name = 'register.html'
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            user_obj = form.save(commit=False)
            user_obj.is_active = False
            
            user_obj.save()
            
            send_otp_email(user_obj)

            return redirect('verify-email')
        
        context = {
            'form':form
        }
        
        return render(request, self.template_name, context)
        
        
class VerifyEmailView(View):

    template_name = 'verify_email.html'
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        
        otp = request.POST.get('otp')
        
        try:
            user_obj = User.objects.get(otp=otp)
        
            user_obj.is_active = True
            user_obj.is_verified = True
            user_obj.otp = None
            
            user_obj.save()
            return redirect('signin')
        
        except:
            
            messages.error(request, 'Invalid OTP')
            
            return render(request, self.template_name)
        
        
class SignInView(View):
    
    template_name = 'signin.html'
    form_class = LoginForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            uname = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password')
            
            user_obj = authenticate(request, username=uname, password=pwd)
            

            
            if user_obj:
                
                login(request, user_obj)
                return redirect('product-list')
            
        return render(request, self.template_name, {'form':form})
    

class SignOutView(View):
    
    def get(self, request, *args, **kwargs):
        
        logout(request)
        
        return redirect('product-list')
    

class ProductListView(View):
    
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        
        qs = Product.objects.all()
        p = Paginator(qs, 8)
        
        wishlit_items_ids = []
        
        if request.user.is_authenticated:
            wishlit_items = request.user.wishlist.wishlist_item.all()
            wishlit_items_ids = [wi.product_object.id for wi in wishlit_items]

        page_number = request.GET.get('page')
        
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
        
        context = {
            # 'products': qs,
            'page_obj': page_obj,
            'wishlist_items_ids': wishlit_items_ids
        }
        
        return render(request, self.template_name, context)
    
    
class ProductDetailView(View):
    
    template_name = 'product_detail.html'
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        product = Product.objects.get(id=id)
        
        context = {
            'product':product
        }

        return render(request, self.template_name, context)
    
    
class ContactView(View):
    
    template_name = 'contacts.html'

    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
    
    
class AddToCartView(View):
    
    template_name = 'product_detail.html'
    
    def post(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        product_obj = Product.objects.get(id=id)
        
        if request.user.is_authenticated:
            
            try:
            
                size = request.POST.get('size')
                quantity = request.POST.get('quantity')
                size_object = Size.objects.get(name=size)
                basket_object = request.user.cart
                
                if BasketItem.objects.filter(product_object=product_obj, is_order_placed=False, size_object=size_object):
                    messages.info(request, 'Already added to cart! Select different size')
                    return redirect('product-detail', id)
                
                BasketItem.objects.create(
                    product_object=product_obj,
                    quantity=quantity,
                    size_object=size_object,
                    basket_object=basket_object
                )
                
                print("Item has been added to cart")
                
                return redirect('cart-summary')
        
            except:
                messages.error(request, "Please select a size!")
                
                context = {
                    'product':product_obj
                }
                
                return render(request, self.template_name, context)
            
        messages.info(request, 'Login or Register for add product to cart')
        return render(request, self.template_name, {'product':product_obj})
        
        
class CartSummaryView(View):
    
    template_name = 'cart_summary.html'

    def get(self, request, *args, **kwargs):
        
        qs = BasketItem.objects.filter(basket_object=request.user.cart, is_order_placed=False)
        
        basket_total = sum([bi.item_total for bi in qs])
        
        total_items = qs.count()
        
        context = {
            'basket_items':qs,
            'basket_total':basket_total,
            'total_items':total_items
        }

        return render(request, self.template_name, context)
    
    
class CartItemDeleteView(View):
    
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        request.user.cart.cart_item.get(id=id).delete()
        
        return redirect('cart-summary')


class WishListView(View):
    
    template_name = 'wishlist.html'

    def get(self, request, *args, **kwargs):
        
        qs = request.user.wishlist.wishlist_item.all()
        
        context = {
            'products': qs
        }
        
        return render(request, self.template_name, context)
    

class AddToWishlist(View):
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        product_obj = Product.objects.get(id=id)
        
        if not WishlistItem.objects.filter(product_object=product_obj):
        
            WishlistItem.objects.create(
                product_object = product_obj,
                whishlist_object = request.user.wishlist
            )
        
        return redirect('product-list')
    

class WishListItemDelete(View):
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        WishlistItem.objects.get(id=id).delete()
        
        return redirect('wishlist')
    
    
class PlaceOrderView(View):
    
    template_name = 'place_order.html'
    form_class = OrderForm
    
    def get(self, request, *args, **kwargs):
        
        form = self.form_class()
        
        qs = request.user.cart.cart_item.filter(is_order_placed=False)
        
        total_order_price = sum([bi.item_total for bi in qs])
        
        context = {
            'form': form,
            'items': qs,
            'total_price': total_order_price
        }
        
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            form.instance.customer = request.user
            order_instance = form.save()
            
            basket_items = request.user.cart.cart_item.filter(is_order_placed=False)
            
            payment_method = form.cleaned_data.get('payment_method')
            print(payment_method)

            for bi in basket_items:
                
                OrderItem.objects.create(
                    order_object = order_instance,
                    product_object = bi.product_object,
                    quantity = bi.quantity,
                    size_object = bi.size_object,
                    price = bi.product_object.price
                )
                
                bi.is_order_placed = True
                bi.save()
                
            if payment_method == "ONLINE":
                
                client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))
                
                amount = sum([bi.item_total for bi in basket_items]) * 100

                data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
                
                payment = client.order.create(data=data)
                
                rzp_order_id = payment.get('id')
                
                order_instance.rzp_order_id = rzp_order_id
                order_instance.save()
                
                name = request.user.username
                email = request.user.email
                phone = request.user.phone
                
                context = {
                    'amount': amount,
                    'key_id': RZP_KEY_ID,
                    'order_id': rzp_order_id,
                    'currency':'INR',
                    'name': name.capitalize(),
                    'email': email,
                    'phone': phone,
                }
                
                return render(request, 'payment.html', context)
            
            return redirect('order-summary')
        

class OrderSummaryView(View):
    
    template_name = 'order_summary.html'

    def get(self, request, *args, **kwargs):
        
        qs = reversed(request.user.orders.all())
        
        return render(request, self.template_name, {'orders': qs})
    

@method_decorator(csrf_exempt, name='dispatch')   
class PaymentVerificationView(View):
    
    def post(self, request, *args, **kwargs):
        
        client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

        try:
            client.utility.verify_payment_signature(request.POST)
            print('payment success')
            
            order_id = request.POST.get('razorpay_order_id')
            order_object = Order.objects.get(rzp_order_id=order_id)
            order_object.is_paid = True
            order_object.save()
            
            # User session may end due to using csrf_exempt. So login again to avoid authentication issue.
            login(request, order_object.customer)
            
        except:
            print('payment failed')
                
        print(request.POST)

        return redirect('order-summary')