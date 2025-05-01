from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Disponibilidad

def index(request):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    franjas = [
        "7:00 am – 9:00 am",
        "9:00 am – 12:00 pm",
        "2:00 pm – 5:00 pm",
        "5:00 pm – 7:00 pm",
        "7:00 pm – 9:00 pm",
        "9:00 pm en adelante"
    ]
    return render(request, 'index.html', {'dias': dias, 'franjas': franjas})


@csrf_exempt
def guardar_disponibilidad(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        dias = request.POST.get('dias_disponibles')
        franjas = request.POST.get('franjas_horarias')
        obs = request.POST.get('observaciones')

        if nombre and dias and franjas:
            Disponibilidad.objects.create(
                nombre=nombre,
                correo=correo,
                dias_disponibles=dias,
                franjas_horarias=franjas,
                observaciones=obs or ''
            )
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error', 'mensaje': 'Campos obligatorios'})
    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'})
