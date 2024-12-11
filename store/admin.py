from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Register Customer model
admin.site.register(Customer)


# Register other models
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
