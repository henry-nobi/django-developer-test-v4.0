# Generated by Django 5.1.4 on 2024-12-15 17:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlanguage',
            name='is_primary',
            field=models.BooleanField(default=False, verbose_name='is primary'),
        ),
        migrations.AlterField(
            model_name='userlanguage',
            name='language_code',
            field=models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('es', 'Spanish'), ('it', 'Italian')], default='en', max_length=10, verbose_name='language code'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userlanguage',
            unique_together={('user_profile', 'language_code')},
        ),
        migrations.AlterUniqueTogether(
            name='userprofile',
            unique_together={('user', 'company')},
        ),
    ]
