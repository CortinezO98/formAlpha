from django.db import models

class Disponibilidad(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True)
    dias_disponibles = models.TextField()
    franjas_horarias = models.TextField()
    observaciones = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def get_dias_display(self):
        return ', '.join(self.dias_disponibles.split(','))

    def get_horarios_display(self):
        return ', '.join(self.franjas_horarias.split(','))

    def __str__(self):
        return self.nombre
