from django import forms
from .models import Service, UserAlert

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            'name',
            'url',
            'interval',
            'is_active',
            'db_username',
            'db_password',
            'db_database',   
        ]
        widgets = {
            'interval': forms.NumberInput(attrs={'min': 1}),
            'db_password': forms.PasswordInput(render_value=True),
        }