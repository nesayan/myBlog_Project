# Generated by Django 3.1.3 on 2020-11-24 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=models.TextField(),
        ),
    ]
