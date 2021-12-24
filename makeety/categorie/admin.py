from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	
	list_display = ('category_name', 'slug', 'is_available')
	prepopulated_fields = {'slug': ('category_name', )}
	list_editable = ('is_available', )

admin.site.register(Category, CategoryAdmin)