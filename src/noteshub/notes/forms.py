from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'color', 'tags', 'file']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'content': forms.Textarea(attrs={'rows': 5}),
        }
