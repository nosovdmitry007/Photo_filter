# Generated by Django 4.0.5 on 2022-06-13 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_search', models.TextField(blank=True, verbose_name='Name search')),
                ('where_search', models.CharField(max_length=32, verbose_name='Where search')),
            ],
            options={
                'verbose_name': 'Params',
            },
        ),
        migrations.CreateModel(
            name='Skills_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skil', models.CharField(max_length=60, verbose_name='Skil')),
            ],
            options={
                'verbose_name': 'Skills table',
                'ordering': ('skil',),
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, verbose_name='name')),
                ('salary', models.CharField(max_length=32, verbose_name='Salary')),
                ('about', models.TextField(blank=True, verbose_name='About')),
                ('link', models.TextField(blank=True, verbose_name='Link')),
                ('comment', models.TextField(blank=True, verbose_name='Commentary')),
                ('date_publik', models.DateField(blank=True, verbose_name='date_publication')),
                ('skils', models.ManyToManyField(to='parserapp.skills_table')),
            ],
            options={
                'verbose_name': 'Vacancys',
                'ordering': ('link',),
            },
        ),
    ]
