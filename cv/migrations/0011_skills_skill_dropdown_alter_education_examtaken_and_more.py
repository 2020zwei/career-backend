# Generated by Django 4.1.3 on 2023-05-10 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0010_education_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='skills',
            name='skill_dropdown',
            field=models.CharField(blank=True, choices=[('1', 'SELF STARTER'), ('2', 'People Skills'), ('3', 'Critical Thinking Skills')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='examtaken',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='school',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='juniorcerttest',
            name='level',
            field=models.CharField(blank=True, choices=[('1', 'Common'), ('2', 'Higher'), ('3', 'Ordinary')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='juniorcerttest',
            name='result',
            field=models.CharField(blank=True, choices=[('1', 'HIGHER MERIT'), ('2', 'MERIT'), ('3', 'ACHIEVED'), ('4', 'PARTIALLY ACHIEVED'), ('5', 'NOT GRADED')], max_length=2, null=True),
        ),
    ]
