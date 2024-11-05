# Generated by Django 5.1.3 on 2024-11-05 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('star_rating', models.IntegerField()),
                ('mobile_phone', models.IntegerField()),
                ('site', models.URLField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Hotel',
            },
        ),
    ]