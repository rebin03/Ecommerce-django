# Generated by Django 5.1.3 on 2024-11-14 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=200)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=200)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=200)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('name', models.CharField(max_length=200)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('picture', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('color', models.CharField(max_length=200)),
                ('brand_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.brand')),
                ('category_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('size_objects', models.ManyToManyField(to='store.size')),
                ('tag_objects', models.ManyToManyField(to='store.tag')),
            ],
            bases=('store.basemodel',),
        ),
    ]