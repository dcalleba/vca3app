# Generated by Django 3.1.4 on 2020-12-07 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visiteur',
            fields=[
                ('pro_id', models.AutoField(primary_key=True, serialize=False)),
                ('ip', models.CharField(default='', max_length=40, verbose_name='IP')),
                ('email', models.EmailField(default='', max_length=40, verbose_name='Email   ')),
                ('page', models.CharField(default='', max_length=40, verbose_name='Page')),
                ('test', models.CharField(default='', max_length=40, verbose_name='Test')),
                ('test2', models.CharField(default='', max_length=40, verbose_name='Test')),
            ],
        ),
    ]
