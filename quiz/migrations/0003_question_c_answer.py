# Generated by Django 5.0.6 on 2024-07-14 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_question_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='c_answer',
            field=models.TextField(default='a', unique=True),
        ),
    ]
