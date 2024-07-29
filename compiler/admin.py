from django.contrib import admin
from .models import compiler_question

# Create a custom admin class for the compiler_question model
class CompilerQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'questions')  # Display the 'id' and 'questions' fields in the list view

admin.site.register(compiler_question, CompilerQuestionAdmin)
