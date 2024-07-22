from django.db import models

class compiler_question(models.Model):
    questions=models.TextField(max_length=300, blank=False, unique=True)

def __str__(self):
        return self.questions
