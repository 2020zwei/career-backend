# Generated by Django 4.1.3 on 2024-11-20 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_student_is_subscribed'),
        ('diary', '0002_alter_workexperiencequestion_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperiencequestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
    ]
