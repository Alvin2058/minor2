# fill models.py
from django.db import models

class FillInTheBlankQuestion(models.Model):
    SUBJECT_CHOICES = [
        ('C', 'C'),
        ('Java', 'Java'),
        ('Python', 'Python'),
    ]
    
    question_text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    question_definition = models.TextField(max_length=500, default='default_value_here')
    hint = models.TextField(max_length=500, blank=True, null=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='Python')

    def __str__(self):
        return self.question_text
