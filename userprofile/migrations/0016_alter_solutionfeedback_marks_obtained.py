# Generated by Django 3.2.7 on 2021-11-25 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0015_auto_20211125_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionfeedback',
            name='marks_obtained',
            field=models.FloatField(default=0.0),
        ),
    ]
