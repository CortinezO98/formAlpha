from django.contrib import admin
from import_export.admin import ExportMixin
from import_export import resources, fields
from import_export.formats.base_formats import XLSX
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
    nombre         = fields.Field(attribute='nombre',         column_name='Nombre completo')
    correo         = fields.Field(attribute='correo',         column_name='Correo')
    fecha_registro = fields.Field(attribute='fecha_registro', column_name='Fecha de registro')
    observaciones  = fields.Field(attribute='observaciones',  column_name='Observaciones')

    class Meta:
        model = Disponibilidad
        export_order = (
            'Nombre completo', 'Correo', 'Fecha de registro',
            *DIAS_SEMANA,
            *FRANJAS,
            'Observaciones',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dia in DIAS_SEMANA:
            self.fields[dia] = fields.Field(column_name=dia)
        for franja in FRANJAS:
            self.fields[franja] = fields.Field(column_name=franja)

    def get_export_fields(self, selected_fields=None):
        campos = [
            self.fields['nombre'],
            self.fields['correo'],
            self.fields['fecha_registro'],
        ] + [self.fields[d] for d in DIAS_SEMANA] \
        + [self.fields[f] for f in FRANJAS] \
        + [self.fields['observaciones']]

        if selected_fields:
            return [f for f in campos if f.column_name in selected_fields]
        return campos

    def export_field(self, field, obj, **kwargs):
        if field.column_name in DIAS_SEMANA:
            return "✅" if field.column_name in obj.get_dias_display().split(", ") else ""
        if field.column_name in FRANJAS:
            return "✅" if field.column_name in obj.get_horarios_display().split(", ") else ""
        return super().export_field(field, obj, **kwargs)


@admin.register(Disponibilidad)
class DisponibilidadAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DisponibilidadResource
    list_display   = ('nombre', 'correo', 'get_dias', 'get_horarios', 'fecha_registro', 'observaciones')
    ordering       = ['-fecha_registro']

    def get_export_formats(self):
        formats = super().get_export_formats()  
        if XLSX not in formats:
            formats.append(XLSX)
        return formats

    def get_dias(self, obj):
        return obj.get_dias_display()
    get_dias.short_description = 'Días disponibles'

    def get_horarios(self, obj):
        return obj.get_horarios_display()
    get_horarios.short_description = 'Horarios disponibles'
