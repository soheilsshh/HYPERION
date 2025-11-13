from django import forms
from .models import Service, UserAlert

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'url', 'interval', 'is_active', 'additional_info']
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 3, 'placeholder': '{"port": 8080}'}),
            'interval': forms.NumberInput(attrs={'min': 1}),
        }