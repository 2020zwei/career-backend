# Generated by Django 4.1.3 on 2024-08-13 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0012_alter_adminlevel5_college_alter_adminlevel5_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminlevel5',
            old_name='url',
            new_name='courseInformation',
        ),
        migrations.RenameField(
            model_name='adminlevel6',
            old_name='url',
            new_name='courseInformation',
        ),
        migrations.RenameField(
            model_name='adminlevel8',
            old_name='url',
            new_name='courseInformation',
        ),
        migrations.RenameField(
            model_name='apprentice',
            old_name='url',
            new_name='courseInformation',
        ),
        migrations.RenameField(
            model_name='level5',
            old_name='url',
            new_name='courseInformation',
        ),
        migrations.RenameField(
            model_name='level6',
            old_name='url',
            new_name='courseInformation',
        ),
        migrations.RenameField(
            model_name='level8',
            old_name='url',
            new_name='courseInformation',
        ),
    ]
