# Generated by Django 5.1.3 on 2024-11-15 04:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('is_order_placed', models.BooleanField(default=False)),
                ('basket_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='store.basket')),
                ('product_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('size_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.size')),
            ],
            bases=('store.basemodel',),
        ),
    ]
