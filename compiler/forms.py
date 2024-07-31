from django import forms

class CodeForm(forms.Form):
    LANGUAGE_CHOICES = [
        ('python3', 'Python'),
        # ('cpp', 'C++'),
        ('java', 'Java'),
        ('c', 'C'),
        # ('php', 'PHP'),
        # ('html', 'HTML'),
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    code = forms.CharField(widget=forms.Textarea(attrs={'id': 'id_code'}))
