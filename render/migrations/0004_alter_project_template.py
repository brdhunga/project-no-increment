# Generated by Django 3.2.18 on 2023-04-29 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render', '0003_alter_project_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='template',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
