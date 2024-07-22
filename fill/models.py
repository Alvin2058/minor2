# fill/models.py

from django.db import models

class Exercise(models.Model):
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    definition = models.TextField(blank=True, null=True)

    SUBJECT_CHOICES = [
        ('C', 'C'),
        ('Python', 'Python'),
        ('Java', 'Java'),
        # Add more subjects as needed
    ]
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='Python')


    def __str__(self):
        return self.question

class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    user_input = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission for Exercise: {self.exercise_id}"
