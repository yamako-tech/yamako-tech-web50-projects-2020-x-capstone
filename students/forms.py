from  django import forms
from .models import MyWord


class MyWordForm(forms.ModelForm):
    class Meta:
        model = MyWord
        fields = ['new_word', 'meaning']
        widgets = {
            'new_word': forms.TextInput(attrs={'class': 'form-control', 'id': 'wordid'}),
            'meaning': forms.TextInput(attrs={'class': 'form-control', 'id': 'meaningid'}),
        }