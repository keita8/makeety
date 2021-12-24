from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [

	path('place_orders/', views.place_orders, name='place_orders'),
	path('payment/', views.payment, name='payment'),

]