# Generated by Django 4.2.10 on 2024-06-12 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=True)),
                ('no', models.CharField(blank=True, default=True)),
            ],
        ),
    ]
