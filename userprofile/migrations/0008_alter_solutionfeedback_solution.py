# Generated by Django 3.2.7 on 2021-10-19 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_alter_solutions_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutionfeedback',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.solutions'),
        ),
    ]
