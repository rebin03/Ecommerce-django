from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from random import randint

# Create your models here.

class User(AbstractUser):
    
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True)
    
    def generate_otp(self):
        
        self.otp = str(randint(1000,9999)) + str(self.id)
        self.save()



class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


class Brand(BaseModel):

    name=models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Size(BaseModel):

    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Category(BaseModel):

    name=models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    

class Tag(BaseModel):

    name=models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(BaseModel):

    title=models.CharField(max_length=200)
    description=models.TextField()
    price=models.PositiveIntegerField()
    picture=models.ImageField(upload_to="product_images", null=True, blank=True)
    brand_object=models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_object=models.ForeignKey(Category, on_delete=models.CASCADE)
    size_objects=models.ManyToManyField(Size)
    tag_objects=models.ManyToManyField(Tag)
    color=models.CharField(max_length=200)


    def __str__(self):
        return self.title


class Basket(BaseModel):

    owner=models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    
    # @property
    # def basket_total(self):
        
    #     items = sel.cart.cart_item
    #     total = 0
        
    #     if items:
    #         total = sum([bi.item_total for bi in items])

    #     return total

# Query to fetch basket of authenticated user

# - Basket.objects.get(owner=request.user)
# - request.user.cart.all()


class BasketItem(BaseModel):

    product_object=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    size_object=models.ForeignKey(Size, on_delete=models.CASCADE)
    is_order_placed=models.BooleanField(default=False)
    basket_object=models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="cart_item")
    
    @property
    def item_total(self):
        
        return self.product_object.price * self.quantity


# Query to fetch basket item to authenticated user

# - BasketItem.objects.filter(basket_object__owner=request.user)
# - request.user.cart.cart_item.filter(is_order_placed=False)


# function to create basket when user is created
def create_basket(sender, instance, created, **kwargs):
    
    if created:
        
        Basket.objects.create(owner=instance)
        

post_save.connect(create_basket, User)