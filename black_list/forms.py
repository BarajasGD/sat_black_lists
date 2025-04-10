from django import forms
from django.core.validators import RegexValidator

class ConsultaForm(forms.Form):
    RFC_VALIDATOR = RegexValidator(
        regex='^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$',
        message='Formato de RFC inválido'
    )
    
    LISTA_OPCIONES = [
        #('Incumplidos', 'Incumplidos'),
        ('NoLocalizados', 'No Localizados'),
        ('Sentencias', 'Sentencias'),
        ('Cancelados', 'Cancelados'),
    ]
    
    rfc = forms.CharField(
        label='RFC',
        max_length=13,
        min_length=12,
        validators=[RFC_VALIDATOR],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: XAXX010101000',
            'autocomplete': 'off'
        })
    )
    
    lista = forms.ChoiceField(
        label='Tipo de lista',
        choices=LISTA_OPCIONES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )