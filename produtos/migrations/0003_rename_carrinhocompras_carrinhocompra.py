# Generated by Django 3.2.7 on 2021-10-08 19:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produtos', '0002_carrinhocompras'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarrinhoCompras',
            new_name='CarrinhoCompra',
        ),
    ]