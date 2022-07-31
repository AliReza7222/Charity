# Generated by Django 4.0.6 on 2022-07-31 06:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charities', '0006_profileuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefactor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='benefactor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='charity',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='charity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='image',
            field=models.ImageField(upload_to='image-profile/'),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]