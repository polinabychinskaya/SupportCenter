# Generated by Django 4.2.7 on 2023-11-16 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_alter_tickets_sender_alter_tickets_supporter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
    ]
