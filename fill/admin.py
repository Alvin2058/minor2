# fill admin.py
from django.contrib import admin
from .models import FillInTheBlankQuestion

@admin.register(FillInTheBlankQuestion)
class FillInTheBlankQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'correct_answer', 'question_definition', 'hint', 'subject')
    search_fields = ('question_text', 'correct_answer', 'question_definition', 'hint', 'subject')
    fields = ('question_text', 'correct_answer', 'question_definition', 'hint', 'subject')
