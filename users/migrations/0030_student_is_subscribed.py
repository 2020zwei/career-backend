# Generated by Django 4.1.3 on 2024-08-13 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_remove_stripecustomer_card_last4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
    ]