from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
	list_display = ['user', 'first_name', 'last_name', 'order_number']

# Register your models here.
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)