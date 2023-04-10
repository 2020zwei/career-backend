# Generated by Django 4.1.3 on 2023-04-10 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apprentice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('level', models.CharField(blank=True, max_length=50, null=True)),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level6', models.BooleanField(default='False')),
                ('Level5', models.BooleanField(default='False')),
                ('level8', models.BooleanField(default='False')),
                ('other', models.BooleanField(default='False')),
                ('apprentice', models.BooleanField(default='False')),
            ],
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.CharField(blank=True, max_length=50, null=True)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='othr', to='choices.choice')),
            ],
        ),
        migrations.CreateModel(
            name='Level8',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('point', models.IntegerField(blank=True, null=True)),
                ('college', models.CharField(blank=True, max_length=50, null=True)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lvl8', to='choices.choice')),
            ],
        ),
        migrations.CreateModel(
            name='Level6',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('point', models.IntegerField(blank=True, null=True)),
                ('college', models.CharField(blank=True, max_length=50, null=True)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lvl6', to='choices.choice')),
            ],
        ),
        migrations.CreateModel(
            name='Level5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('college', models.CharField(blank=True, max_length=50, null=True)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lvl5', to='choices.choice')),
            ],
        ),
    ]
