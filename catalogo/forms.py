from django.forms import ModelForm
from .models import paciente

class productoForm(ModelForm):
    class Meta:
        model = paciente
        fields = ['nombre', 'apellidos', 'direccion', 'ciudad', 'telefono', 'historial_clinico']