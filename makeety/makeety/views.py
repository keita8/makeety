from django.http import HttpResponse
from django.shortcuts import render, redirect
from store.models import Product

def homepage(request):

	product = Product.objects.filter(is_available=True)

	template_name = 'pages/homepage.html'
	context = {

		'product' : product,
	}

	return render(request, template_name , context)