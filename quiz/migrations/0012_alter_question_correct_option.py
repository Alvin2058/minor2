# Generated by Django 5.0.6 on 2024-08-04 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_remove_question_creator_attemptedquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct_option',
            field=models.CharField(choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')], max_length=1),
        ),
    ]
