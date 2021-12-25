from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
class Payment(models.Model):
	user           = models.ForeignKey(Account, on_delete=models.CASCADE)
	payment_id     = models.CharField(max_length=100, verbose_name="ID paiement")
	payment_method = models.CharField(max_length=100, verbose_name="Moyen de paiement")
	amount_paid    = models.CharField(max_length=100)
	status         = models.CharField(max_length=100)
	created_at     = models.DateTimeField(auto_now_add=True, verbose_name="Paiement effectué")

	class Meta:
		verbose_name = "Paiement"
		verbose_name_plural = "Paiement"

	def __str__(self):
		return self.payment_id

class Order(models.Model):
	STATUS = (

		('Nouvelle', 'Nouvelle'),
		('Acceptée', 'Acceptée'),
		('Terminée', 'Terminée'),
		('Annulée', 'Annulée'),
	)

	user           = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
	payment        = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Paiement")
	order_number   = models.CharField(max_length=20, verbose_name="Numero de la commande")
	first_name     = models.CharField(max_length=50, verbose_name="Prenom")
	last_name      = models.CharField(max_length=50, verbose_name="Nom")
	phone          = models.CharField(max_length=15, verbose_name="Telephone")
	email          = models.EmailField(max_length=50, verbose_name="Email")
	address_line_1 = models.CharField(max_length=50, verbose_name="Adresse 1")
	address_line_2 = models.CharField(max_length=50, blank=True, verbose_name="Adresse 2")
	country        = models.CharField(max_length=50, verbose_name="Pays")
	state          = models.CharField(max_length=50, verbose_name="Etat")
	city           = models.CharField(max_length=50, verbose_name="Ville")
	order_note     = models.CharField(max_length=200, blank=True, verbose_name="Note de la commande")
	order_total    = models.FloatField(verbose_name="Commande totale")
	tax            = models.FloatField(verbose_name="Taxe")
	status         = models.CharField(max_length=20, choices=STATUS, default="Nouvelle")
	ip             = models.CharField(max_length=10, blank=True)
	is_ordered     = models.BooleanField(default=False, verbose_name='Commande deja effectuée ?')
	created_at     = models.DateTimeField(auto_now_add=True, verbose_name="Crée le")
	updated_at     = models.DateTimeField(auto_now=True, verbose_name="Modifié le")


	class Meta:
		verbose_name = "Commande"
		verbose_name_plural = "Commandes"


	def __str__(self):
		return f" {self.first_name}  {self.last_name} {self.user}"

	@property
	def full_name(self):
		return f" {self.first_name} {self.last_name}"

	@property
	def full_address(self):
		return f" {self.address_line_1} {self.address_line_2} "

class OrderProduct(models.Model):
	user           = models.ForeignKey(Account, on_delete=models.CASCADE)
	order          = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Commande")
	payment        = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Paiement")
	product        = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Article")
	variation      = models.ForeignKey(Variation, on_delete=models.CASCADE, verbose_name="Caracteristiques de l'article")
	color          = models.CharField(max_length=50, verbose_name="Couleur")
	size           = models.CharField(max_length=50, verbose_name="Taille")
	quantity       = models.IntegerField(verbose_name="Quantité")
	product_price  = models.FloatField(verbose_name="Prix du l'article")
	ordered        = models.BooleanField(default=False, verbose_name="Deja commandé ?")
	created_at     = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
	updated_at     = models.DateTimeField(auto_now=True, verbose_name="Modifié le ")

	class Meta:
		verbose_name = "Produit"
		verbose_name_plural = "Produits"

	def __str__(self):
		return self.product.product_name

