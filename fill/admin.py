from django.contrib import admin
from .models import Exercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_answer', 'definition')
    search_fields = ('question', 'correct_answer')
    list_filter = ('correct_answer',)

    fieldsets = (
        (None, {
            'fields': ('question', 'correct_answer')
        }),
        ('Additional Info', {
            'fields': ('definition',),
            'classes': ('collapse',)  # Optional: Hide this section by default
        }),
    )

