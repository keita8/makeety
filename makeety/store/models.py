from django.db import models
from categorie.models import Category
from django.urls import reverse
from datetime import datetime
# Create your models here.

class Product(models.Model):

    features_choices=(
		('Cruise Control', 'Cruise Control'),
		('Audio Interface', 'Audio Interface'),
		('Airbags', 'Airbags'),
		('Air Conditioning', 'Air Conditioning'),
		('Seat Heating', 'Seat Heating'),
		('Alarm System', 'Alarm System'),
		('ParkAssist', 'ParkAssist'),
		('Power Steering', 'Power Steering'),
		('Reversing Camera', 'Reversing Camera'),
		('Direct Fuel Injection', 'Direct Fuel Injection'),
		('Auto Start/Stop', 'Auto Start/Stop'),
		('Wind Deflector', 'Wind Deflector'),
		('Bluetooth Handset', 'Bluetooth Handset'),
    )


    state_choice = (
        ('GN', 'GUINEE'),
        ('US', 'USA'),
        ('FR', 'FRANCE'),
        ('MA', 'MAROC'),
        ('CA', 'CANADA'),
        ('BR', 'BRESIL'),
        ('AR', 'ARGENTINE'),
        ('DE', 'ALLEMAGNE'),
        ('IT', 'ITALIE'),
        ('ES', 'ESPAGNE'),
        ('PT', 'PORTUGAL'),
        ('RU', 'RUSSIE'),
        ('IN', 'INDE'),
        ('ID', 'INDONESIE'),
        ('IN', 'Indiana'),
        ('MY', 'MALAYSIE'),
        ('CN', 'CHINE'),
        ('JP', 'JAPON'),
        ('UK', 'ANGLETERRE'),
        ('NL', 'PAYS BAS'),
        ('BE', 'BELGIQUE'),
    )



    condition_choice = (

    	('Nouveau', 'Nouveau'),
    	('En solde', 'En solde'),

    )

    year_choice = []

    for r in range(2000, (datetime.now().year+1)): 
    	year_choice.append((r,r))

    product_name  = models.CharField(max_length=200, verbose_name="Article")
    slug          = models.SlugField(max_length=200)
    description   = models.TextField()
    manufacturer  = models.CharField(choices=state_choice, max_length=50, blank=True, verbose_name='Fabricant')
    condition     = models.CharField(choices=condition_choice, max_length=200, blank=True)
    year          = models.IntegerField(('Année'), choices=year_choice, default='2021')
    price         = models.FloatField(verbose_name='Prix', default=0.0)
    price         = models.FloatField(verbose_name='Prix', default=0.0)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categorie de l\'article')
    features      = models.CharField(choices=features_choices, blank=True, verbose_name='Caracteristiques', max_length=200)
    specification = models.TextField(blank=True, null=True)
    photo         = models.ImageField()
    image1        = models.ImageField(blank=True)
    image2        = models.ImageField(blank=True)
    image3        = models.ImageField(blank=True)
    image4        = models.ImageField(blank=True)
    stock         = models.IntegerField(default=0)
    is_available  = models.BooleanField(default=True, verbose_name='Disponible ?')
    free_shipping = models.BooleanField(default=False, verbose_name='Livraison gratuite ?')
    created_date  = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    modified_date = models.DateTimeField(auto_now=True,verbose_name='Modifié le')

    class Meta:
    	ordering = ['-created_date']
    	verbose_name = 'Article'
    	verbose_name_plural = 'Articles'

    def get_url(self):
    	return reverse('store:product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
    	return self.product_name



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='couleur', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='taille', is_active=True)

variation_category_choice = (
    ('couleur', 'couleur'),
    ('taille', 'taille'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Article")
    variation_category = models.CharField(max_length=100, choices=variation_category_choice, verbose_name="Caracteristiques")
    variation_value     = models.CharField(max_length=100, verbose_name="valeur de la caracteristique")
    is_active           = models.BooleanField(default=True, verbose_name="Deja active ?")
    created_date        = models.DateTimeField(auto_now=True, verbose_name="Date de creation")

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class Banner(models.Model):
    image1 = models.ImageField(upload_to='banner/images')
    image2 = models.ImageField(upload_to='banner/images')

    class Meta:
        verbose_name = "Bannière"
        verbose_name_plural = "Bannières"
