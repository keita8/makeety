from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, first_name, last_name, username, email, password=None):
		if not email:
			raise ValueError("L'adresse email est requise ")

		if not username:
			raise ValueError("Vous devez fournir un nom d'utilisateur")

		user = self.model(

			email      = self.normalize_email(email),
			first_name = first_name,
			last_name  = last_name,
			username   = username,

			)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, first_name, last_name, username, email, password):

		user = self.create_user(

			email      = self.normalize_email(email),
			first_name = first_name,
			last_name  = last_name,
			username   = username,
			password   = password,

			)

		user.is_active 	   = True
		user.is_admin  	   = True
		user.is_staff  	   = True
		user.is_superadmin = True

		user.save(using=self._db)

		return user






class Account(AbstractBaseUser):
	first_name = models.CharField(max_length=200, verbose_name='Prenom')
	last_name  = models.CharField(max_length=200,verbose_name='Nom')
	username   = models.CharField(max_length=50, unique=True, verbose_name='Pseudo')
	email      = models.EmailField(max_length=200, verbose_name='email', unique=True)
	phone      = models.CharField(max_length=50, verbose_name='telephone')

	date_joined 	= models.DateTimeField(auto_now_add=True, verbose_name='Creation')
	last_joined 	= models.DateTimeField(auto_now_add=True, verbose_name='Dernière connexion')
	is_admin    	= models.BooleanField(default=False, verbose_name='Admin')
	is_staff    	= models.BooleanField(default=False, verbose_name='Membre')
	is_active   	= models.BooleanField(default=False, verbose_name='Actif')
	is_superadmin   = models.BooleanField(default=False)

	USERNAME_FIELD  = 'email'
	REQUIRED_FIELDS = ['username' ,'first_name', 'last_name']

	objects = MyAccountManager()

	class Meta:
		verbose_name = 'Compte'
		verbose_name_plural = 'Comptes'

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True




