# Generated by Django 3.2.7 on 2021-10-05 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_course_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseuserrelation',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]
