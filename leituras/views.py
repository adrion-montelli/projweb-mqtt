from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.core.management import call_command
from datetime import datetime
from urllib.parse import urlencode
import csv
import io
from .models import DadosAgregados


def index(request):
    """View principal para listar dados agregados com filtros"""
    query = DadosAgregados.objects.all()
    
    # Aplica filtros
    query = apply_filters(query, request)
    
    # Ordena antes de aplicar o slice
    query = query.order_by('-periodo_inicio')
    
    # Conta o total ANTES de aplicar o slice (garante contagem correta)
    total_leituras = query.count()
    
    # Aplica limite apenas se não houver filtro de data
    if not request.GET.get('data_inicio') and not request.GET.get('data_fim'):
        leituras = list(query[:24])  # Converte para lista para exibição
    else:
        leituras = list(query)  # Converte para lista para exibição
    
    # Busca dados para preencher os filtros
    clientes = DadosAgregados.objects.values_list('id_cliente', flat=True).distinct().order_by('id_cliente')
    equipamentos = DadosAgregados.objects.values_list('id_equipamento', flat=True).distinct().order_by('id_equipamento')
    
    # Busca o timestamp da última agregação
    ultima_atualizacao = DadosAgregados.objects.order_by('-updated_at').first()
    ultima_atualizacao = ultima_atualizacao.updated_at if ultima_atualizacao else None
    
    # Detecta quais colunas têm dados
    colunas_visiveis = detectar_colunas_visiveis(leituras)
    
    # Obter nome do equipamento selecionado
    nome_equipamento = None
    if request.GET.get('id_equipamento'):
        nome_equipamento = obter_nome_equipamento(request.GET.get('id_equipamento'))
    
    context = {
        'leituras': leituras,
        'total_leituras': total_leituras,  # Usa o count feito antes do slice
        'clientes': clientes,
        'equipamentos': equipamentos,
        'filters': request.GET,
        'ultima_atualizacao': ultima_atualizacao,
        'colunas_visiveis': colunas_visiveis,
        'nome_equipamento': nome_equipamento,
    }
    
    return render(request, 'leituras/index.html', context)


def apply_filters(query, request):
    """Aplica filtros de busca"""
    if request.GET.get('id_cliente'):
        query = query.filter(id_cliente=request.GET.get('id_cliente'))
    
    if request.GET.get('id_equipamento'):
        query = query.filter(id_equipamento=request.GET.get('id_equipamento'))
    
    if request.GET.get('data_inicio'):
        data_inicio = datetime.strptime(request.GET.get('data_inicio'), '%Y-%m-%d')
        data_inicio = timezone.make_aware(data_inicio.replace(hour=0, minute=0, second=0))
        query = query.filter(periodo_inicio__gte=data_inicio)
    
    if request.GET.get('data_fim'):
        data_fim = datetime.strptime(request.GET.get('data_fim'), '%Y-%m-%d')
        data_fim = timezone.make_aware(data_fim.replace(hour=23, minute=59, second=59))
        query = query.filter(periodo_inicio__lte=data_fim)
    
    return query


def detectar_colunas_visiveis(leituras):
    """Detecta quais colunas têm dados para otimizar a exibição"""
    colunas = {
        'brunidores': False,
        'descascadores': False,
        'polidores': False,
        'temperatura': False,
        'umidade': False,
        'grandezas_eletricas': False,
    }
    
    for leitura in leituras:
        if leitura.corrente_brunidores_media is not None:
            colunas['brunidores'] = True
        if leitura.corrente_descascadores_media is not None:
            colunas['descascadores'] = True
        if leitura.corrente_polidores_media is not None:
            colunas['polidores'] = True
        if leitura.temperatura_media is not None:
            colunas['temperatura'] = True
        if leitura.umidade_media is not None:
            colunas['umidade'] = True
        if leitura.tensao_r_media is not None:
            colunas['grandezas_eletricas'] = True
    
    return colunas


def obter_nome_equipamento(id_equipamento):
    """Formata o nome do equipamento"""
    partes = id_equipamento.split('_')
    
    if len(partes) >= 2:
        tipo = partes[0].capitalize()
        numero = partes[1].zfill(2)
        return f"{tipo} {numero}"
    
    return id_equipamento


def agregar(request):
    """Executa o comando de agregação de dados"""
    if request.method == 'POST':
        call_command('agregar_leituras', periodo='hora')
        messages.success(request, 'Dados atualizados com sucesso!')
        
        # Preserva os filtros que vieram no POST (campos hidden)
        query_params = {}
        if request.POST.get('id_cliente'):
            query_params['id_cliente'] = request.POST.get('id_cliente')
        if request.POST.get('id_equipamento'):
            query_params['id_equipamento'] = request.POST.get('id_equipamento')
        if request.POST.get('data_inicio'):
            query_params['data_inicio'] = request.POST.get('data_inicio')
        if request.POST.get('data_fim'):
            query_params['data_fim'] = request.POST.get('data_fim')
        
        # Constrói a URL com os parâmetros
        if query_params:
            return redirect(f"/?{urlencode(query_params)}")
        return redirect('/')
    
    # Se for GET, mantém os filtros da URL
    query_params = request.GET.copy()
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}?{query_params.urlencode()}")


def exportar(request):
    """Exporta dados agregados para CSV"""
    query = DadosAgregados.objects.all()
    query = apply_filters(query, request)
    leituras = query.order_by('periodo_inicio')
    
    # Cria o arquivo CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="dados_agregados_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv"'
    
    # Adiciona BOM para UTF-8
    response.write('\ufeff')
    
    writer = csv.writer(response, delimiter=';')
    
    # Escreve cabeçalho
    if leituras.exists():
        primeira_leitura = leituras.first()
        campos = [field.name for field in primeira_leitura._meta.fields]
        writer.writerow(campos)
        
        # Escreve dados
        for leitura in leituras:
            valores = [getattr(leitura, campo) for campo in campos]
            writer.writerow(valores)
    
    return response
