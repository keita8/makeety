from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class MyAccountManager(BaseUserManager):
	def create_user(self, first_name, last_name, username, email, city, password = None):
		if not email:
			raise ValueError("Vous devez fournir un email")
		if not username:
			raise ValueError("Vous devez fournir un pseudonyme")

		user = self.model(

			email = self.normalize_email(email),
			username = username,
			first_name = first_name,
			last_name = last_name,
			city = city,

			)
		user.set_password(password)
		user.save(using=self._db)

		return user 

	def create_superuser(self, first_name, last_name,username, city, email, password):
		user = self.create_user(
			email = self.normalize_email(email),
			username=username,
			password=password,
			city=city,
			first_name=first_name,
			last_name=last_name,

		)

		user.is_admin = True
		user.is_active = True
		user.is_staff = True
		user.is_superadmin = True

		user.save(using=self._db)

		return user




class Account(AbstractBaseUser):
	first_name = models.CharField('Prenom', max_length=60)
	last_name = models.CharField('Nom', max_length=60)
	username = models.CharField('Pseudo', max_length=25, unique=True)
	email = models.EmailField(max_length=200, unique=True)
	city = models.CharField('Ville/Région', max_length=200, blank=True)
	# phone_number = PhoneNumberField()
	phone_number = models.CharField('Téléphone', max_length=60)


	date_joined = models.DateTimeField('Creation', auto_now_add=True)
	last_login = models.DateTimeField('Dernière connexion', auto_now_add=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active =models.BooleanField(default=False)
	is_superadmin =models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [ 'first_name', 'last_name', 'username', 'city']

	objects = MyAccountManager()

	class Meta:
		verbose_name = 'compte'
		verbose_name_plural = 'compte'

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True

