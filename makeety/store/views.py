from django.shortcuts import render, get_object_or_404
from .models import Product
from categorie.models import Category

# Create your views here.

def store(request, category_slug=None):

	category = None
	product  = None

	if category_slug != None:
		category = get_object_or_404(Category, slug = category_slug)
		product  = Product.objects.filter(category=category, is_available=True)
		product_count = product.count()

	else:
		product = Product.objects.filter(is_available=True)
		product_count     = product.count()


	template_name = 'store/store.html'
	context = {
      
      'available_product' : product,
      'product_count'     : product_count,

	}

	return render(request, template_name, context)


def product_detail(request, category_slug, product_slug):

	try:
		product_detail = Product.objects.get(category__slug=category_slug, slug=product_slug)
	except Exception as e:
		raise e


	template_name = 'store/product_detail.html'
	context       = {
		'product_detail' : product_detail,
	}


	return render(request, template_name, context)