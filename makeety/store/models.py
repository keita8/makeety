from django.db import models
from categorie.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):

	product_name = models.CharField(max_length=100, verbose_name='Nom du produit')
	slug         = models.SlugField(max_length=100)
	description  = models.TextField(max_length=500, blank=True)
	price        = models.FloatField(default=0.0, verbose_name='Prix')
	photo        = models.ImageField(upload_to='photos/produits')
	stock        = models.IntegerField()
	is_available = models.BooleanField(default=True, verbose_name='Disponible ?')
	category     = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='categorie')
	created_date = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ajout')
	modified_date= models.DateTimeField(auto_now=True, verbose_name='Dernière modification')

	class Meta:
		verbose_name = 'Produit'
		verbose_name_plural = 'Produits'

	def get_url(self):
		return reverse('store:product_detail', args=[self.category.slug, self.slug])

	def __str__(self):
		return self.product_name
