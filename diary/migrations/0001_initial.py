# Generated by Django 4.1.3 on 2024-11-19 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0030_student_is_subscribed'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkExperienceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Day 1', 'Day 1'), ('Day 2', 'Day 2'), ('Day 3', 'Day 3'), ('Day 4', 'Day 4'), ('Day 5', 'Day 5'), ('Day 6', 'Day 6'), ('Day 7', 'Day 7'), ('Day 8', 'Day 8'), ('Day 9', 'Day 9'), ('Day 10', 'Day 10')], max_length=25)),
                ('date', models.DateField()),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
        ),
    ]
