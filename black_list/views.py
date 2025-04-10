from django.http import HttpResponse
import subprocess
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import ConsultaForm
import os
import logging
from .sat_utils import consultar_lista_sat  # Nueva función específica
# Create your views here.


def index(request):
    return render(request, "black_list/index.html")


logger = logging.getLogger(__name__)

def verification(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            rfc = form.cleaned_data['rfc']
            lista_seleccionada = form.cleaned_data['lista']
            
            try:
                # Consultar solo la lista seleccionada
                resultado = consultar_lista_sat(rfc, lista_seleccionada)
                
                if resultado['error']:
                    messages.error(request, f"Error al consultar {lista_seleccionada}: {resultado['error']}")
                else:
                    return render(request, 'black_list/results.html', {
                        'rfc': rfc,
                        'lista_consultada': lista_seleccionada,
                        'resultado': resultado
                    })
                    
            except Exception as e:
                logger.error(f"Error en consulta: {str(e)}")
                messages.error(request, "Error interno al procesar la consulta")
                
            return redirect('verification')  # Recargar para mostrar mensajes
            
    else:
        form = ConsultaForm()
    
    return render(request, 'black_list/verification.html', {'form': form})