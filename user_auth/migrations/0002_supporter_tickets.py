# Generated by Django 4.2.7 on 2023-11-07 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Processing', 'Processing')], default='Available', max_length=64, verbose_name='Status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=2048, verbose_name='Problem desciption')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('Processing', 'Processing'), ('Frozen', 'Frozen'), ('Done', 'Done')], default='New', max_length=64, verbose_name='Status')),
                ('sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
                ('supporter', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_auth.supporter', verbose_name='Supporter')),
            ],
        ),
    ]
