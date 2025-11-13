from django.contrib import admin
from .models import (
    CorrenteBrunidores, 
    CorrenteDescascadores, 
    CorrentePolidores,
    Temperatura, 
    Umidade, 
    GrandezaEletrica, 
    DadosAgregados
)

@admin.register(DadosAgregados)
class DadosAgregadosAdmin(admin.ModelAdmin):
    list_display = ['id_cliente', 'id_equipamento', 'periodo_inicio', 'periodo_fim', 'registros_contagem']
    list_filter = ['id_cliente', 'id_equipamento', 'periodo_inicio']
    search_fields = ['id_cliente', 'id_equipamento']

admin.site.register(CorrenteBrunidores)
admin.site.register(CorrenteDescascadores)
admin.site.register(CorrentePolidores)
admin.site.register(Temperatura)
admin.site.register(Umidade)
admin.site.register(GrandezaEletrica)
