from django.http import HttpResponse
from django.shortcuts import render, redirect
from store.models import Product
from categorie.models import Category

def homepage(request):

	products = Product.objects.filter(is_available=True)[:12]
	categories = Category.objects.filter(is_available=True)[:3]

	# print([x for x in categories])
	for cat in categories:
		for product in cat.product_set.all():
			print(product.product_name)



	template_name = 'pages/homepage.html'
	context = {

		'products' : products,
		'categories': categories,
	}

	return render(request, template_name , context)