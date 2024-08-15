# Generated by Django 4.1.3 on 2024-08-15 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0013_rename_url_adminlevel5_courseinformation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminlevel5',
            old_name='courseInformation',
            new_name='course_information',
        ),
        migrations.RenameField(
            model_name='adminlevel6',
            old_name='courseInformation',
            new_name='course_information',
        ),
        migrations.RenameField(
            model_name='adminlevel8',
            old_name='courseInformation',
            new_name='course_information',
        ),
        migrations.RenameField(
            model_name='apprentice',
            old_name='courseInformation',
            new_name='course_information',
        ),
        migrations.RenameField(
            model_name='level5',
            old_name='courseInformation',
            new_name='course_information',
        ),
        migrations.RenameField(
            model_name='level6',
            old_name='courseInformation',
            new_name='course_information',
        ),
        migrations.RenameField(
            model_name='level8',
            old_name='courseInformation',
            new_name='course_information',
        ),
        migrations.AlterField(
            model_name='level5',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='level6',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='level8',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
