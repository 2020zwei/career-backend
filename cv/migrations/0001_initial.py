# Generated by Django 4.1.3 on 2023-04-10 05:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objective', models.TextField(max_length=300)),
                ('is_juniorcert_test', models.BooleanField(default=False)),
                ('skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('HobbiesandInterests', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
                ('school', models.CharField(max_length=50)),
                ('examtaken', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField()),
                ('enddate', models.DateField()),
                ('jobtitle', models.CharField(choices=[('1', 'ASSISTANT'), ('2', 'WORK SHADOW'), ('3', 'OTHER')], max_length=1)),
                ('company', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='JuniorCertTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('1', 'ENGLISH'), ('2', 'MATHEMATICS'), ('3', 'IRISH'), ('4', 'ACCOUNTING'), ('5', 'AGRICULTURAL ECONOMICS'), ('6', 'AGRICULTURAL SCIENCE'), ('7', 'ANCIENT_GREEK'), ('8', 'APPLIED MATHEMATICS'), ('9', 'ARABIC'), ('10', 'ART'), ('11', 'BIOLOGY'), ('12', 'BULGARIAN'), ('13', 'BUSINESS'), ('14', 'CHEMISTRY'), ('15', 'CLASSICAL STUDIES'), ('16', 'CONSTRUCTION STUDIES'), ('17', 'CZECH'), ('18', 'DANISH'), ('19', 'DESIGN & COMMUNICATION GRAPHICS'), ('20', 'DUTCH'), ('21', 'ECONOMICS'), ('22', 'ENGINEERING'), ('23', 'ESTONIAN'), ('24', 'FINNISH'), ('25', 'FRENCH'), ('26', 'GEOGRAPHY'), ('27', 'GERMAN'), ('28', 'HEBREW STUDIES'), ('29', 'HISTORY'), ('30', 'HOME ECONOMICS'), ('31', 'HUNGARIAN'), ('32', 'ITALIAN'), ('33', 'JAPANESE'), ('34', 'LATIN'), ('35', 'LATVIAN'), ('36', 'LINK MODULES'), ('37', 'LITHUANIAN'), ('38', 'MALTESE'), ('39', 'MODERN GREEK'), ('40', 'MUSIC'), ('41', 'PHYSICS'), ('42', 'PHYSICS & CHEMISTRY'), ('43', 'POLISH'), ('44', 'POLITICS & SOCIETY'), ('45', 'PORTUGESE'), ('46', 'RELIGIOUS EDUCATION'), ('47', 'ROMANIAN'), ('48', 'RUSSIAN'), ('49', 'SLOVAKIAN'), ('50', 'SLOVENIAN'), ('51', 'SPANISH'), ('52', 'SWEDISH'), ('53', 'TECHNOLOGY')], max_length=2)),
                ('level', models.CharField(choices=[('1', 'Common'), ('2', 'Higher'), ('3', 'Ordinary')], max_length=2)),
                ('result', models.CharField(choices=[('1', 'HIGHER MERIT'), ('2', 'MERIT'), ('3', 'ACHIEVED'), ('4', 'PARTIALLY ACHIEVED'), ('5', 'NOT GRADED')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='LeavingCertTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('1', 'ENGLISH'), ('2', 'MATHEMATICS'), ('3', 'IRISH'), ('4', 'ACCOUNTING'), ('5', 'AGRICULTURAL ECONOMICS'), ('6', 'AGRICULTURAL SCIENCE'), ('7', 'ANCIENT_GREEK'), ('8', 'APPLIED MATHEMATICS'), ('9', 'ARABIC'), ('10', 'ART'), ('11', 'BIOLOGY'), ('12', 'BULGARIAN'), ('13', 'BUSINESS'), ('14', 'CHEMISTRY'), ('15', 'CLASSICAL STUDIES'), ('16', 'CONSTRUCTION STUDIES'), ('17', 'CZECH'), ('18', 'DANISH'), ('19', 'DESIGN & COMMUNICATION GRAPHICS'), ('20', 'DUTCH'), ('21', 'ECONOMICS'), ('22', 'ENGINEERING'), ('23', 'ESTONIAN'), ('24', 'FINNISH'), ('25', 'FRENCH'), ('26', 'GEOGRAPHY'), ('27', 'GERMAN'), ('28', 'HEBREW STUDIES'), ('29', 'HISTORY'), ('30', 'HOME ECONOMICS'), ('31', 'HUNGARIAN'), ('32', 'ITALIAN'), ('33', 'JAPANESE'), ('34', 'LATIN'), ('35', 'LATVIAN'), ('36', 'LINK MODULES'), ('37', 'LITHUANIAN'), ('38', 'MALTESE'), ('39', 'MODERN GREEK'), ('40', 'MUSIC'), ('41', 'PHYSICS'), ('42', 'PHYSICS & CHEMISTRY'), ('43', 'POLISH'), ('44', 'POLITICS & SOCIETY'), ('45', 'PORTUGESE'), ('46', 'RELIGIOUS EDUCATION'), ('47', 'ROMANIAN'), ('48', 'RUSSIAN'), ('49', 'SLOVAKIAN'), ('50', 'SLOVENIAN'), ('51', 'SPANISH'), ('52', 'SWEDISH'), ('53', 'TECHNOLOGY')], max_length=2)),
                ('level', models.CharField(choices=[('1', 'HIGHER'), ('2', 'ORDINARY'), ('3', 'COMMON')], max_length=2)),
                ('result', models.CharField(choices=[('1', 'PENDING'), ('2', 'H1'), ('3', 'H2'), ('4', 'H3'), ('5', 'H4'), ('6', 'H5'), ('7', 'H6'), ('8', 'H7'), ('9', 'O1'), ('10', 'O2'), ('11', 'O3'), ('12', 'O4'), ('13', 'O5'), ('14', 'O6'), ('15', 'O7')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Qualities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quality', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'qualities',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_title', models.CharField(choices=[('1', 'MR'), ('2', 'MRS'), ('3', 'MS')], max_length=1)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('organization_address', models.CharField(blank=True, max_length=50, null=True)),
                ('area_code', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=300)),
            ],
            options={
                'verbose_name_plural': 'skills',
            },
        ),
    ]
