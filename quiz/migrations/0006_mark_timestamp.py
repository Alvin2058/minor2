# Generated by Django 5.0.6 on 2024-07-28 08:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_question_c_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
