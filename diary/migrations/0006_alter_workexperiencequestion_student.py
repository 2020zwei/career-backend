# Generated by Django 4.1.3 on 2024-11-20 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diary', '0005_workexperiencequestion_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperiencequestion',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]