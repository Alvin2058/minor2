# Generated by Django 5.0.6 on 2024-07-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fill', '0002_exercise_definition'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='subject',
            field=models.CharField(choices=[('C', 'C'), ('Python', 'Python'), ('Java', 'Java')], default='Python', max_length=50),
        ),
    ]
