from django.shortcuts import render, get_object_or_404
from .models import Product
from categorie.models import Category
from carts.views import _cart_id
from carts.models import CartItem, Cart
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 

# Create your views here.

def store(request, category_slug=None):

	category = None
	product  = None

	if category_slug != None:
		category = get_object_or_404(Category, slug = category_slug)
		product  = Product.objects.filter(category=category, is_available=True)
		paginator = Paginator(product, 6) # afficher 6 articles par page
		page = request.GET.get('page')
		paged_products = paginator.get_page(page)
		product_count = product.count()

	else:
		product = Product.objects.all().filter(is_available=True).order_by('id')
		paginator = Paginator(product, 6) # afficher 6 articles par page
		page = request.GET.get('page')
		paged_products = paginator.get_page(page)
		product_count     = product.count()


	template_name = 'store/store.html'
	context = {
      
      'available_product' : paged_products,
      'product_count'     : product_count,

	}

	return render(request, template_name, context)


def product_detail(request, category_slug, product_slug):

	try:
		product_detail = Product.objects.get(category__slug=category_slug, slug=product_slug)
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product_detail).exists()

	except Exception as e:
		raise e


	template_name = 'store/product_detail.html'
	context       = {
		'product_detail' : product_detail,
		'product_already_in_cart': in_cart,
	}


	return render(request, template_name, context)


def search(request):

	product = None

	if 'keyword' in request.GET:
		keyword = request.GET['keyword']

		if keyword:
			product = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
			product_count = product.count()

	template_name = 'store/store.html'
	context = {
		'available_product' : product,
		'product_count' : product_count,
	}
	return render(request, template_name, context)