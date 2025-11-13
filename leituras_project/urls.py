"""
URL configuration for leituras_project project.

Estrutura de URLs:
- /admin/ - Painel administrativo Django
- /accounts/ - URLs de autenticação (login, logout, password reset)
- /dashboard/ - Dashboard principal
- /api/ - Endpoints de API para dados dos gráficos
- / - Redirecionamento para dashboard
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Avg, Count, Max
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import timedelta
from django.utils import timezone
from leituras.models import DadosAgregados


@login_required
def dashboard_view(request):
    """
    View para o dashboard principal com dados resumidos.
    
    Context:
        - total_leituras: Número total de registros
        - media_temperatura: Temperatura média
        - ultima_leitura: Último registro inserido
        - leituras: Últimas 10 leituras agregadas (com filtros aplicados)
        - clientes: Lista de clientes únicos
        - equipamentos: Lista de equipamentos únicos
    """
    # Obter parâmetros de filtro da request
    id_cliente = request.GET.get('id_cliente', '').strip()
    id_equipamento = request.GET.get('id_equipamento', '').strip()
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()
    
    # Query base
    queryset = DadosAgregados.objects.all()
    
    # Aplicar filtros
    if id_cliente:
        queryset = queryset.filter(id_cliente=id_cliente)
    if id_equipamento:
        queryset = queryset.filter(id_equipamento=id_equipamento)
    if data_inicio:
        from datetime import datetime
        try:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            queryset = queryset.filter(periodo_inicio__gte=data_inicio_dt)
        except ValueError:
            pass
    if data_fim:
        from datetime import datetime
        try:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            # Adiciona 1 dia para incluir todo o dia final
            from datetime import timedelta
            data_fim_dt = data_fim_dt + timedelta(days=1)
            queryset = queryset.filter(periodo_fim__lt=data_fim_dt)
        except ValueError:
            pass
    
    # Consultas para os cards de resumo
    total_leituras = queryset.count()
    
    summary = queryset.aggregate(
        media_temp=Avg('temperatura_media'),
        max_temp=Max('temperatura_max'),
    )
    
    ultima_leitura = queryset.order_by('-updated_at').first()
    
    # Últimas 10 leituras para a tabela
    leituras = queryset.order_by('-periodo_fim')[:10]
    
    # Dados para filtros (sempre mostrar todas as opções)
    clientes_all = DadosAgregados.objects.values_list('id_cliente', flat=True).distinct()
    equipamentos_all = DadosAgregados.objects.values_list('id_equipamento', flat=True).distinct()

    context = {
        'total_leituras': total_leituras,
        'media_temperatura': summary.get('media_temp'),
        'ultima_leitura': ultima_leitura,
        'leituras': leituras,
        'clientes': clientes_all,
        'equipamentos': equipamentos_all,
        # Manter filtros selecionados no formulário
        'filtro_cliente': id_cliente,
        'filtro_equipamento': id_equipamento,
        'filtro_data_inicio': data_inicio,
        'filtro_data_fim': data_fim,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
@require_http_methods(["GET"])
def chart_data_view(request):
    """
    Endpoint de API para fornecer dados dos gráficos.
    
    Query Parameters:
        - range: Período de dados ('7d', '30d', '90d') - padrão: '30d'
        - cliente: ID do cliente para filtrar
        - equipamento: ID do equipamento para filtrar
    
    Response JSON:
        {
            'labels': [...],              # Labels para o eixo X (datas/horas)
            'temperatura_media': [...],   # Dados de temperatura média
            'corrente_brunidores': [...] # Dados de corrente brunidores
        }
    """
    try:
        # Parâmetros da requisição
        range_param = request.GET.get('range', '30d')
        cliente = request.GET.get('cliente')
        equipamento = request.GET.get('equipamento')
        
        # Calcular data de início baseada no range
        hoje = timezone.now()
        range_map = {
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
            '90d': timedelta(days=90),
        }
        data_inicio = hoje - range_map.get(range_param, timedelta(days=30))
        
        # Query base
        queryset = DadosAgregados.objects.filter(
            periodo_fim__gte=data_inicio
        ).order_by('periodo_fim')
        
        # Aplicar filtros se fornecidos
        if cliente:
            queryset = queryset.filter(id_cliente=cliente)
        if equipamento:
            queryset = queryset.filter(id_equipamento=equipamento)
        
        # Limitar últimas 50 leituras para performance
        leituras = list(queryset[:50])
        
        # Preparar dados para o gráfico
        labels = [
            leitura.periodo_fim.strftime("%d/%m %H:%M") 
            for leitura in leituras
        ]
        
        temperatura_media = [
            float(leitura.temperatura_media) if leitura.temperatura_media else 0 
            for leitura in leituras
        ]
        
        corrente_brunidores = [
            float(leitura.corrente_brunidores_media) if leitura.corrente_brunidores_media else 0 
            for leitura in leituras
        ]
        
        return JsonResponse({
            'success': True,
            'labels': labels,
            'temperatura_media': temperatura_media,
            'corrente_brunidores': corrente_brunidores,
            'count': len(leituras),
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=400)


@login_required
@require_http_methods(["GET"])
def chart_data_summary_view(request):
    """
    Endpoint de API para dados resumidos (totais, médias, máximos).
    
    Query Parameters:
        - range: Período de dados ('7d', '30d', '90d') - padrão: '30d'
    
    Response JSON:
        {
            'total_registros': número,
            'temperatura_media': float,
            'temperatura_maxima': float,
            'corrente_brunidores_media': float,
            'data_atualizacao': datetime
        }
    """
    try:
        range_param = request.GET.get('range', '30d')
        
        # Calcular período
        hoje = timezone.now()
        range_map = {
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
            '90d': timedelta(days=90),
        }
        data_inicio = hoje - range_map.get(range_param, timedelta(days=30))
        
        # Query com aggregação
        queryset = DadosAgregados.objects.filter(
            periodo_fim__gte=data_inicio
        )
        
        summary = queryset.aggregate(
            total=Count('id'),
            temp_media=Avg('temperatura_media'),
            temp_max=Max('temperatura_max'),
            corrente_brunidores_media=Avg('corrente_brunidores_media'),
        )
        
        ultima = queryset.order_by('-periodo_fim').first()
        
        return JsonResponse({
            'success': True,
            'total_registros': summary['total'] or 0,
            'temperatura_media': round(float(summary['temp_media'] or 0), 2),
            'temperatura_maxima': float(summary['temp_max'] or 0),
            'corrente_brunidores_media': round(float(summary['corrente_brunidores_media'] or 0), 2),
            'data_atualizacao': ultima.periodo_fim.isoformat() if ultima else None,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
        }, status=400)


# URL Patterns
urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # URLs de Autenticação (login, logout, password reset)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # URLs da App Leituras
    path('leituras/', include('leituras.urls')),
    
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # API Endpoints
    path('api/chart-data/', chart_data_view, name='chart-data'),
    path('api/chart-summary/', chart_data_summary_view, name='chart-summary'),
    
    # Redirecionamento da raiz para dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=True)),
]
