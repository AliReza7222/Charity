# Generated by Django 4.0.6 on 2022-07-26 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charities', '0004_alter_task_charity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='charity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charities.charity'),
        ),
    ]
