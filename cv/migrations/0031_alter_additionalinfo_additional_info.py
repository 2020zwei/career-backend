# Generated by Django 4.1.3 on 2024-01-22 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0030_alter_additionalinfo_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalinfo',
            name='additional_info',
            field=models.TextField(default='Any further information which might support an application such as\n          membership of an organisation or the ability to speak another\n          language.', max_length=300),
        ),
    ]
