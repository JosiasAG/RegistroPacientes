from django.db import models

class paciente(models.Model):
    nombre= models.CharField(max_length=50)
    apellidos=models.CharField(max_length=100)
    direccion=models.CharField(max_length=150)
    ciudad=models.CharField(max_length=50)
    telefono=models.CharField(max_length=20)
    ingreso=models.DateTimeField()
    alta=models.DateTimeField()
    historial_clinico=models.TextField()
    
    def __str__(self):
        return self.nombre
