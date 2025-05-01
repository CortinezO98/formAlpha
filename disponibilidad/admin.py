from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources, fields
from .models import Disponibilidad

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
FRANJAS = [
    "7:00 am – 9:00 am",
    "9:00 am – 12:00 pm",
    "2:00 pm – 5:00 pm",
    "5:00 pm – 7:00 pm",
    "7:00 pm – 9:00 pm",
    "9:00 pm en adelante",
]

class DisponibilidadResource(resources.ModelResource):
    nombre = fields.Field(attribute='nombre', column_name='Nombre completo')
    correo = fields.Field(attribute='correo', column_name='Correo')
    fecha_registro = fields.Field(attribute='fecha_registro', column_name='Fecha de registro')
    observaciones = fields.Field(attribute='observaciones', column_name='Observaciones')

    def __init__(self):
        super().__init__()
        for dia in DIAS_SEMANA:
            self.fields[dia] = fields.Field(column_name=dia)
        for franja in FRANJAS:
            self.fields[franja] = fields.Field(column_name=franja)

    def get_export_fields(self):
        base_fields = [
            self.fields['nombre'],
            self.fields['correo'],
            self.fields['fecha_registro'],
        ]
        dias_fields = [self.fields[d] for d in DIAS_SEMANA]
        franjas_fields = [self.fields[f] for f in FRANJAS]
        base_fields += dias_fields + franjas_fields
        base_fields.append(self.fields['observaciones'])
        return base_fields

    def export_field(self, field, obj):
        if field.column_name in DIAS_SEMANA:
            return "✅" if field.column_name in obj.get_dias_display().split(", ") else ""
        elif field.column_name in FRANJAS:
            return "✅" if field.column_name in obj.get_horarios_display().split(", ") else ""
        else:
            return super().export_field(field, obj)

    class Meta:
        model = Disponibilidad

@admin.register(Disponibilidad)
class DisponibilidadAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DisponibilidadResource
    list_display = ('nombre', 'correo', 'get_dias', 'get_horarios', 'fecha_registro', 'observaciones')
    ordering = ['-fecha_registro']

    def get_dias(self, obj):
        return obj.get_dias_display()
    get_dias.short_description = 'Días disponibles'

    def get_horarios(self, obj):
        return obj.get_horarios_display()
    get_horarios.short_description = 'Horarios disponibles'
