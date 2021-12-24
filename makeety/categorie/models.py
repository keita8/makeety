from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
	category_name = models.CharField(max_length=70, verbose_name='Nom de la categorie', unique=True)
	slug = models.SlugField(max_length=70, unique=True)
	overview = models.TextField(verbose_name="Aperçu")
	description = models.TextField(max_length=300)
	is_available = models.BooleanField(default=False, verbose_name="Disponible ?")
	categories_image = models.ImageField(upload_to='photos/categorie', blank=True,verbose_name='image')

	class Meta:
		verbose_name = 'categorie'
		verbose_name_plural = 'categories'

	def get_url(self):
		return reverse('store:product_by_category', args=[self.slug])


	def __str__(self):
		return self.category_name
