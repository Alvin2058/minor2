# Generated by Django 5.0.6 on 2024-07-31 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_remove_question_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='creator',
        ),
    ]
