# Generated by Django 2.2.10 on 2021-04-25 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('ecom', '0007_remove_orders_distribuidor'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='distribuidor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
