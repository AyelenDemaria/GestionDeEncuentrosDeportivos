from django.contrib import admin
from .models import Inscripcion
# Register your models here.

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'jugador', 'partido', 'fecha_hora_inscripcion', 'fecha_hora_baja')
    list_filter = ('partido', 'jugador')
    #search_fields = ('partido','jugador')
admin.site.register(Inscripcion, InscripcionAdmin)
