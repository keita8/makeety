# Generated by Django 3.2.4 on 2021-12-23 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=250, verbose_name='ID du panier')),
                ('date_added', models.DateField(auto_now_add=True, verbose_name="Date d'ajout")),
            ],
            options={
                'verbose_name': 'Panier',
                'verbose_name_plural': 'Paniers',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='quantité')),
                ('is_active', models.BooleanField(default=True, verbose_name='Article du panier actif ?')),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carts.cart', verbose_name='Panier')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
                ('variations', models.ManyToManyField(blank=True, to='store.Variation', verbose_name='Caracteristiques')),
            ],
            options={
                'verbose_name': 'Article au panier',
                'verbose_name_plural': 'Articles au panier',
            },
        ),
    ]
