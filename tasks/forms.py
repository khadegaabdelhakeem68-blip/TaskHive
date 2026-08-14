from django import forms
from .models import Task, Bid

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Web Development, Design'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount', 'message']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }