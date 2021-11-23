from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [

	path('register/', views.register, name='register'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),

	path('', views.dashboard, name='dashboard'),
	path('dashboard/', views.dashboard, name='dashboard'),

	path('forget_password/', views.forget_password, name='forget_password'),
	path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
	path('reset_password/', views.reset_password, name='reset_password'),
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]