# Generated by Django 4.0.6 on 2022-07-27 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_re_password_alter_user_gender_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='re_password',
        ),
    ]
