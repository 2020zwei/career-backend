# Generated by Django 4.1.3 on 2024-08-12 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_school_category_stripecustomer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stripecustomer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
