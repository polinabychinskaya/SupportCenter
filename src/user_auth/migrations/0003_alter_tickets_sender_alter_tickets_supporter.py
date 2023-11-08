# Generated by Django 4.2.7 on 2023-11-08 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_supporter_tickets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='supporter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_auth.supporter', verbose_name='Supporter'),
        ),
    ]