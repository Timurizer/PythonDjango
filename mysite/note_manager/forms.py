from django import forms
from .models import *


class NoteForm(forms.ModelForm):
    note_header = forms.CharField(max_length=30, help_text="Please enter the note header.")
    note_body = forms.CharField(max_length=200, help_text="Please enter the note body.")

    category = forms.CharField(max_length=30, help_text="Please enter the note body.")

    class Meta:
        model = Note
        fields = ('note_header', 'note_body', 'category')  # 'pub_date', 'category', 'user')
