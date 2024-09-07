from django import forms
from .models import Ingreso, Gasto, CategoriaGasto, Ahorro, Inversion, Presupuesto, Deuda, Transaccion

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['monto', 'fuente']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'fuente': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['monto', 'categoria', 'descripcion']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoriaGastoForm(forms.ModelForm):
    class Meta:
        model = CategoriaGasto
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AhorroForm(forms.ModelForm):
    class Meta:
        model = Ahorro
        fields = ['monto_objetivo', 'monto_actual', 'descripcion', 'fecha_fin']
        widgets = {
            'monto_objetivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class InversionForm(forms.ModelForm):
    class Meta:
        model = Inversion
        fields = ['monto', 'tipo', 'descripcion']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['categoria', 'monto', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class DeudaForm(forms.ModelForm):
    class Meta:
        model = Deuda
        fields = ['monto', 'descripcion', 'fecha', 'fecha_vencimiento', 'estado']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['monto', 'tipo', 'categoria', 'descripcion']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }
