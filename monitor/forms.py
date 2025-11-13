from django import forms
from .models import Service, UserAlert

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'url', 'interval', 'is_active']
        widgets = {
            'interval': forms.NumberInput(attrs={'min': 1}),
        }