#quiz models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question = models.TextField(blank=False, unique=True)
    option1 = models.CharField(blank=False, max_length=150)
    option2 = models.CharField(blank=False, max_length=150)
    option3 = models.CharField(blank=False, max_length=150)
    option4 = models.CharField(blank=False, max_length=150)
    correct_option = models.CharField(max_length=1, blank=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    c_answer = models.CharField(max_length=250, blank=False) 

    # Define choices for subject field
    SUBJECT_CHOICES = [
        ('C', 'C'),
        ('Python', 'Python'),
        ('Java', 'Java'),
        # Add more subjects as needed
    ]

    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES,default="Python")

    def __str__(self):
        return f"Question({self.question}, {self.creator})"

class Mark(models.Model):
    total = models.IntegerField(blank=False)
    got = models.IntegerField(blank=False, default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Mark({self.got}/{self.total}, {self.user})"
