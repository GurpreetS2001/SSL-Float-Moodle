# Generated by Django 3.2.7 on 2021-10-20 12:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_alter_solutionfeedback_solution'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsvFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_csv', models.FileField(blank=True, null=True, upload_to='assignments/csv', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])])),
                ('active', models.BooleanField(default=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.assignments')),
            ],
        ),
    ]
