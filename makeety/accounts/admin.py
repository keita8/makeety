from django.contrib import admin
from .models import Account, MyAccountManager
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):
	list_display 	   = ('email', 'first_name', 'last_name', 'city', 'phone_number', 'last_login', 'date_joined','is_active')
	list_display_links = ('email', 'first_name', 'last_name')
	readonly_fields    = ('last_login', 'date_joined')
	ordering           = ('-date_joined',)
	filter_horizontal  = ()
	list_filter        = ()
	fieldsets          = ()
	# list_editable = ('is_active', )




admin.site.register(Account, AccountAdmin)
