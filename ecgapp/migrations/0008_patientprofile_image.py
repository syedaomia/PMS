# Generated by Django 3.2 on 2021-04-26 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecgapp', '0007_auto_20210424_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]