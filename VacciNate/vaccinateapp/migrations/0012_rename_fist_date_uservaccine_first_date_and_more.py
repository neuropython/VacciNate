# Generated by Django 5.0.2 on 2024-04-28 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccinateapp', '0011_alter_vaccine_obligation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uservaccine',
            old_name='fist_date',
            new_name='first_date',
        ),
        migrations.AlterField(
            model_name='uservaccine',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
