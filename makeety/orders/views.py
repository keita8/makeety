from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def place_orders(request, total=0, quantity=0):

	current_user = request.user

	# si dans le panier il n'y a pas d'article on redirige vers la page shopping
	cart_items = CartItem.objects.filter(user=current_user)
	cart_count = cart_items.count()

	if cart_count <= 0:
		return redirect('store:product')

	grand_total = 0
	tax = 0

	for cart_item in cart_items:
		total += (cart_item.product.price * cart_item.quantity)
		quantity += cart_item.quantity
	

	tax = (2 * total)/100
	grand_total = total + tax



	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			# stocker toutes les informations sur la facturation dans un tableau de type commande
			data = Order()
			data.user           = current_user
			data.first_name     = form.cleaned_data['first_name']
			data.last_name      = form.cleaned_data['last_name']
			data.phone          = form.cleaned_data['phone']
			data.email          = form.cleaned_data['email']
			data.city           = form.cleaned_data['city']
			data.country        = form.cleaned_data['country']
			data.state          = form.cleaned_data['state']
			data.order_note     = form.cleaned_data['order_note']
			data.address_line_1 = form.cleaned_data['address_line_1']
			data.address_line_2 = form.cleaned_data['address_line_2']
			data.order_total    = grand_total
			data.tax            = tax
			data.ip             = request.META.get('REMOTE_ADDR')

			data.save()
			yr = int(datetime.date.today().strftime('%Y'))
			dt = int(datetime.date.today().strftime('%d'))
			mt = int(datetime.date.today().strftime('%m'))
			d = datetime.date(yr,mt,dt)
			current_date = d.strftime("%Y%m%d") #20210305
			order_number = current_date + str(data.id)
			data.order_number = order_number
			data.save()

			order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number )

			template_name = 'orders/payment.html'
			context = {
				'order': order,
				'cart_items': cart_items,
				'grand_total' : grand_total,
				'tax' : tax,
				'total' : total,
			}

			return render(request, template_name, context)
	else:
		return redirect('carts:checkout')


def payment(request):

	template_name = 'orders/payment.html'
	context = {}


	return render(request, template_name, context)