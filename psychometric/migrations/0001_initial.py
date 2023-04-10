# Generated by Django 4.1.3 on 2023-04-10 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=300)),
                ('weightage', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PsychometricTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(null=True)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='psychometric.psychometrictest')),
            ],
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='TestResultDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='psychometric.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='psychometric.question')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psychometric.testresult')),
            ],
        ),
    ]
