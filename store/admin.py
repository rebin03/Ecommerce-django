from django.contrib import admin
from store.models import User, Product, Brand, Category, Size, Tag

# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Tag)