from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Avg, Max, Min, Count
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from leituras.models import (
    CorrenteBrunidores, CorrenteDescascadores, CorrentePolidores,
    Temperatura, Umidade, GrandezaEletrica, DadosAgregados
)


class Command(BaseCommand):
    help = 'Agrega leituras dos sensores em intervalos de tempo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--periodo',
            type=str,
            default='hora',
            choices=['hora', 'dia', 'semana'],
            help='Período de agregação (hora, dia, semana)'
        )

    def handle(self, *args, **options):
        periodo = options['periodo']
        
        self.stdout.write(self.style.SUCCESS(f'Iniciando agregação por {periodo}...'))
        
        # Detecta o backend do banco de dados
        is_mysql = connection.vendor == 'mysql'
        if is_mysql:
            self.stdout.write(self.style.WARNING('Usando SQL otimizado para MySQL'))
        else:
            self.stdout.write(self.style.WARNING('Usando Django ORM (compatível com SQLite)'))
        
        # Define o intervalo baseado no período
        if periodo == 'hora':
            intervalo = timedelta(hours=1)
        elif periodo == 'dia':
            intervalo = timedelta(days=1)
        else:  # semana
            intervalo = timedelta(weeks=1)
        
        # Executa agregação para cada tabela
        if is_mysql:
            self.agregar_corrente_brunidores_mysql(intervalo)
            self.agregar_corrente_descascadores_mysql(intervalo)
            self.agregar_corrente_polidores_mysql(intervalo)
            self.agregar_temperaturas_mysql(intervalo)
            self.agregar_umidades_mysql(intervalo)
            self.agregar_grandezas_eletricas_mysql(intervalo)
        else:
            self.agregar_corrente_brunidores_orm(intervalo)
            self.agregar_corrente_descascadores_orm(intervalo)
            self.agregar_corrente_polidores_orm(intervalo)
            self.agregar_temperaturas_orm(intervalo)
            self.agregar_umidades_orm(intervalo)
            self.agregar_grandezas_eletricas_orm(intervalo)
        
        self.stdout.write(self.style.SUCCESS('Agregação concluída com sucesso!'))

    # ========== Implementação MySQL (SQL otimizado) ==========
    
    def agregar_corrente_brunidores_mysql(self, intervalo):
        """Agrega dados de corrente dos brunidores usando SQL MySQL"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados_agregados (
                    id_cliente, id_equipamento, periodo_inicio, periodo_fim,
                    corrente_brunidores_media, corrente_brunidores_max, 
                    corrente_brunidores_min, corrente_brunidores_ultima,
                    registros_contagem, created_at, updated_at
                )
                SELECT 
                    id_cliente,
                    id_equipamento,
                    DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') as periodo_inicio,
                    DATE_FORMAT(timestamp + INTERVAL 1 HOUR, '%%Y-%%m-%%d %%H:00:00') as periodo_fim,
                    AVG(corrente) as corrente_brunidores_media,
                    MAX(corrente) as corrente_brunidores_max,
                    MIN(corrente) as corrente_brunidores_min,
                    (SELECT corrente FROM corrente_brunidores cb2 
                     WHERE cb2.id_cliente = cb.id_cliente 
                     AND cb2.id_equipamento = cb.id_equipamento
                     AND DATE_FORMAT(cb2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(cb.timestamp, '%%Y-%%m-%%d %%H:00:00')
                     ORDER BY cb2.timestamp DESC LIMIT 1) as corrente_brunidores_ultima,
                    COUNT(*) as registros_contagem,
                    NOW() as created_at,
                    NOW() as updated_at
                FROM corrente_brunidores cb
                WHERE agregado = 0
                GROUP BY id_cliente, id_equipamento, DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00')
                ON DUPLICATE KEY UPDATE
                    corrente_brunidores_media = VALUES(corrente_brunidores_media),
                    corrente_brunidores_max = VALUES(corrente_brunidores_max),
                    corrente_brunidores_min = VALUES(corrente_brunidores_min),
                    corrente_brunidores_ultima = VALUES(corrente_brunidores_ultima),
                    registros_contagem = VALUES(registros_contagem),
                    updated_at = NOW()
            """)
            
            cursor.execute("UPDATE corrente_brunidores SET agregado = 1 WHERE agregado = 0")

    def agregar_corrente_descascadores_mysql(self, intervalo):
        """Agrega dados de corrente dos descascadores usando SQL MySQL"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados_agregados (
                    id_cliente, id_equipamento, periodo_inicio, periodo_fim,
                    corrente_descascadores_media, corrente_descascadores_max, 
                    corrente_descascadores_min, corrente_descascadores_ultima,
                    registros_contagem, created_at, updated_at
                )
                SELECT 
                    id_cliente,
                    id_equipamento,
                    DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') as periodo_inicio,
                    DATE_FORMAT(timestamp + INTERVAL 1 HOUR, '%%Y-%%m-%%d %%H:00:00') as periodo_fim,
                    AVG(corrente) as corrente_descascadores_media,
                    MAX(corrente) as corrente_descascadores_max,
                    MIN(corrente) as corrente_descascadores_min,
                    (SELECT corrente FROM corrente_descascadores cd2 
                     WHERE cd2.id_cliente = cd.id_cliente 
                     AND cd2.id_equipamento = cd.id_equipamento
                     AND DATE_FORMAT(cd2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(cd.timestamp, '%%Y-%%m-%%d %%H:00:00')
                     ORDER BY cd2.timestamp DESC LIMIT 1) as corrente_descascadores_ultima,
                    COUNT(*) as registros_contagem,
                    NOW() as created_at,
                    NOW() as updated_at
                FROM corrente_descascadores cd
                WHERE agregado = 0
                GROUP BY id_cliente, id_equipamento, DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00')
                ON DUPLICATE KEY UPDATE
                    corrente_descascadores_media = VALUES(corrente_descascadores_media),
                    corrente_descascadores_max = VALUES(corrente_descascadores_max),
                    corrente_descascadores_min = VALUES(corrente_descascadores_min),
                    corrente_descascadores_ultima = VALUES(corrente_descascadores_ultima),
                    updated_at = NOW()
            """)
            
            cursor.execute("UPDATE corrente_descascadores SET agregado = 1 WHERE agregado = 0")

    def agregar_corrente_polidores_mysql(self, intervalo):
        """Agrega dados de corrente dos polidores usando SQL MySQL"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados_agregados (
                    id_cliente, id_equipamento, periodo_inicio, periodo_fim,
                    corrente_polidores_media, corrente_polidores_max, 
                    corrente_polidores_min, corrente_polidores_ultima,
                    registros_contagem, created_at, updated_at
                )
                SELECT 
                    id_cliente,
                    id_equipamento,
                    DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') as periodo_inicio,
                    DATE_FORMAT(timestamp + INTERVAL 1 HOUR, '%%Y-%%m-%%d %%H:00:00') as periodo_fim,
                    AVG(corrente) as corrente_polidores_media,
                    MAX(corrente) as corrente_polidores_max,
                    MIN(corrente) as corrente_polidores_min,
                    (SELECT corrente FROM corrente_polidores cp2 
                     WHERE cp2.id_cliente = cp.id_cliente 
                     AND cp2.id_equipamento = cp.id_equipamento
                     AND DATE_FORMAT(cp2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(cp.timestamp, '%%Y-%%m-%%d %%H:00:00')
                     ORDER BY cp2.timestamp DESC LIMIT 1) as corrente_polidores_ultima,
                    COUNT(*) as registros_contagem,
                    NOW() as created_at,
                    NOW() as updated_at
                FROM corrente_polidores cp
                WHERE agregado = 0
                GROUP BY id_cliente, id_equipamento, DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00')
                ON DUPLICATE KEY UPDATE
                    corrente_polidores_media = VALUES(corrente_polidores_media),
                    corrente_polidores_max = VALUES(corrente_polidores_max),
                    corrente_polidores_min = VALUES(corrente_polidores_min),
                    corrente_polidores_ultima = VALUES(corrente_polidores_ultima),
                    updated_at = NOW()
            """)
            
            cursor.execute("UPDATE corrente_polidores SET agregado = 1 WHERE agregado = 0")

    def agregar_temperaturas_mysql(self, intervalo):
        """Agrega dados de temperatura usando SQL MySQL"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados_agregados (
                    id_cliente, id_equipamento, periodo_inicio, periodo_fim,
                    temperatura_media, temperatura_max, 
                    temperatura_min, temperatura_ultima,
                    registros_contagem, created_at, updated_at
                )
                SELECT 
                    id_cliente,
                    id_equipamento,
                    DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') as periodo_inicio,
                    DATE_FORMAT(timestamp + INTERVAL 1 HOUR, '%%Y-%%m-%%d %%H:00:00') as periodo_fim,
                    AVG(temperatura) as temperatura_media,
                    MAX(temperatura) as temperatura_max,
                    MIN(temperatura) as temperatura_min,
                    (SELECT temperatura FROM temperaturas t2 
                     WHERE t2.id_cliente = t.id_cliente 
                     AND t2.id_equipamento = t.id_equipamento
                     AND DATE_FORMAT(t2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(t.timestamp, '%%Y-%%m-%%d %%H:00:00')
                     ORDER BY t2.timestamp DESC LIMIT 1) as temperatura_ultima,
                    COUNT(*) as registros_contagem,
                    NOW() as created_at,
                    NOW() as updated_at
                FROM temperaturas t
                WHERE agregado = 0
                GROUP BY id_cliente, id_equipamento, DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00')
                ON DUPLICATE KEY UPDATE
                    temperatura_media = VALUES(temperatura_media),
                    temperatura_max = VALUES(temperatura_max),
                    temperatura_min = VALUES(temperatura_min),
                    temperatura_ultima = VALUES(temperatura_ultima),
                    updated_at = NOW()
            """)
            
            cursor.execute("UPDATE temperaturas SET agregado = 1 WHERE agregado = 0")

    def agregar_umidades_mysql(self, intervalo):
        """Agrega dados de umidade usando SQL MySQL"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados_agregados (
                    id_cliente, id_equipamento, periodo_inicio, periodo_fim,
                    umidade_media, umidade_max, 
                    umidade_min, umidade_ultima,
                    registros_contagem, created_at, updated_at
                )
                SELECT 
                    id_cliente,
                    id_equipamento,
                    DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') as periodo_inicio,
                    DATE_FORMAT(timestamp + INTERVAL 1 HOUR, '%%Y-%%m-%%d %%H:00:00') as periodo_fim,
                    AVG(umidade) as umidade_media,
                    MAX(umidade) as umidade_max,
                    MIN(umidade) as umidade_min,
                    (SELECT umidade FROM umidades u2 
                     WHERE u2.id_cliente = u.id_cliente 
                     AND u2.id_equipamento = u.id_equipamento
                     AND DATE_FORMAT(u2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(u.timestamp, '%%Y-%%m-%%d %%H:00:00')
                     ORDER BY u2.timestamp DESC LIMIT 1) as umidade_ultima,
                    COUNT(*) as registros_contagem,
                    NOW() as created_at,
                    NOW() as updated_at
                FROM umidades u
                WHERE agregado = 0
                GROUP BY id_cliente, id_equipamento, DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00')
                ON DUPLICATE KEY UPDATE
                    umidade_media = VALUES(umidade_media),
                    umidade_max = VALUES(umidade_max),
                    umidade_min = VALUES(umidade_min),
                    umidade_ultima = VALUES(umidade_ultima),
                    updated_at = NOW()
            """)
            
            cursor.execute("UPDATE umidades SET agregado = 1 WHERE agregado = 0")

    def agregar_grandezas_eletricas_mysql(self, intervalo):
        """Agrega dados de grandezas elétricas usando SQL MySQL"""
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dados_agregados (
                    id_cliente, id_equipamento, periodo_inicio, periodo_fim,
                    tensao_r_media, tensao_r_max, tensao_r_min, tensao_r_ultima,
                    tensao_s_media, tensao_s_max, tensao_s_min, tensao_s_ultima,
                    tensao_t_media, tensao_t_max, tensao_t_min, tensao_t_ultima,
                    corrente_r_media, corrente_r_max, corrente_r_min, corrente_r_ultima,
                    corrente_s_media, corrente_s_max, corrente_s_min, corrente_s_ultima,
                    corrente_t_media, corrente_t_max, corrente_t_min, corrente_t_ultima,
                    potencia_ativa_media, potencia_ativa_max, potencia_ativa_min, potencia_ativa_ultima,
                    potencia_reativa_media, potencia_reativa_max, potencia_reativa_min, potencia_reativa_ultima,
                    fator_potencia_media, fator_potencia_max, fator_potencia_min, fator_potencia_ultima,
                    registros_contagem, created_at, updated_at
                )
                SELECT 
                    id_cliente,
                    id_equipamento,
                    DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00') as periodo_inicio,
                    DATE_FORMAT(timestamp + INTERVAL 1 HOUR, '%%Y-%%m-%%d %%H:00:00') as periodo_fim,
                    AVG(tensao_r), MAX(tensao_r), MIN(tensao_r),
                    (SELECT tensao_r FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(tensao_s), MAX(tensao_s), MIN(tensao_s),
                    (SELECT tensao_s FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(tensao_t), MAX(tensao_t), MIN(tensao_t),
                    (SELECT tensao_t FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(corrente_r), MAX(corrente_r), MIN(corrente_r),
                    (SELECT corrente_r FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(corrente_s), MAX(corrente_s), MIN(corrente_s),
                    (SELECT corrente_s FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(corrente_t), MAX(corrente_t), MIN(corrente_t),
                    (SELECT corrente_t FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(potencia_ativa), MAX(potencia_ativa), MIN(potencia_ativa),
                    (SELECT potencia_ativa FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(potencia_reativa), MAX(potencia_reativa), MIN(potencia_reativa),
                    (SELECT potencia_reativa FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    AVG(fator_potencia), MAX(fator_potencia), MIN(fator_potencia),
                    (SELECT fator_potencia FROM grandezas_eletricas ge2 WHERE ge2.id_cliente = ge.id_cliente AND ge2.id_equipamento = ge.id_equipamento AND DATE_FORMAT(ge2.timestamp, '%%Y-%%m-%%d %%H:00:00') = DATE_FORMAT(ge.timestamp, '%%Y-%%m-%%d %%H:00:00') ORDER BY ge2.timestamp DESC LIMIT 1),
                    COUNT(*) as registros_contagem,
                    NOW() as created_at,
                    NOW() as updated_at
                FROM grandezas_eletricas ge
                WHERE agregado = 0
                GROUP BY id_cliente, id_equipamento, DATE_FORMAT(timestamp, '%%Y-%%m-%%d %%H:00:00')
                ON DUPLICATE KEY UPDATE
                    tensao_r_media = VALUES(tensao_r_media),
                    tensao_r_max = VALUES(tensao_r_max),
                    tensao_r_min = VALUES(tensao_r_min),
                    tensao_r_ultima = VALUES(tensao_r_ultima),
                    updated_at = NOW()
            """)
            
            cursor.execute("UPDATE grandezas_eletricas SET agregado = 1 WHERE agregado = 0")

    # ========== Implementação ORM (compatível com SQLite e MySQL) ==========
    
    def _format_periodo(self, timestamp, intervalo):
        """Formata timestamp para início do período"""
        if intervalo == timedelta(hours=1):
            # Arredonda para a hora
            return timestamp.replace(minute=0, second=0, microsecond=0)
        elif intervalo == timedelta(days=1):
            # Arredonda para o dia
            return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # semana
            # Arredonda para o início da semana (segunda-feira)
            days_since_monday = timestamp.weekday()
            return (timestamp - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    def agregar_corrente_brunidores_orm(self, intervalo):
        """Agrega dados de corrente dos brunidores usando Django ORM"""
        registros = CorrenteBrunidores.objects.filter(agregado=False)
        
        # Agrupa por cliente, equipamento e período
        grupos = {}
        for registro in registros:
            periodo_inicio = self._format_periodo(registro.timestamp, intervalo)
            periodo_fim = periodo_inicio + intervalo
            chave = (registro.id_cliente, registro.id_equipamento, periodo_inicio)
            
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append(registro)
        
        # Processa cada grupo
        for (id_cliente, id_equipamento, periodo_inicio), grupo_registros in grupos.items():
            periodo_fim = periodo_inicio + intervalo
            valores = [r.corrente for r in grupo_registros]
            
            # Busca ou cria registro agregado
            agregado, created = DadosAgregados.objects.get_or_create(
                id_cliente=id_cliente,
                id_equipamento=id_equipamento,
                periodo_inicio=periodo_inicio,
                defaults={
                    'periodo_fim': periodo_fim,
                    'corrente_brunidores_media': sum(valores) / len(valores),
                    'corrente_brunidores_max': max(valores),
                    'corrente_brunidores_min': min(valores),
                    'corrente_brunidores_ultima': grupo_registros[-1].corrente,
                    'registros_contagem': len(grupo_registros),
                }
            )
            
            if not created:
                # Atualiza registro existente
                agregado.corrente_brunidores_media = sum(valores) / len(valores)
                agregado.corrente_brunidores_max = max(valores)
                agregado.corrente_brunidores_min = min(valores)
                agregado.corrente_brunidores_ultima = grupo_registros[-1].corrente
                agregado.registros_contagem = len(grupo_registros)
                agregado.save()
        
        # Marca como agregado
        CorrenteBrunidores.objects.filter(agregado=False).update(agregado=True)

    def agregar_corrente_descascadores_orm(self, intervalo):
        """Agrega dados de corrente dos descascadores usando Django ORM"""
        registros = CorrenteDescascadores.objects.filter(agregado=False)
        
        grupos = {}
        for registro in registros:
            periodo_inicio = self._format_periodo(registro.timestamp, intervalo)
            periodo_fim = periodo_inicio + intervalo
            chave = (registro.id_cliente, registro.id_equipamento, periodo_inicio)
            
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append(registro)
        
        for (id_cliente, id_equipamento, periodo_inicio), grupo_registros in grupos.items():
            periodo_fim = periodo_inicio + intervalo
            valores = [r.corrente for r in grupo_registros]
            
            agregado, created = DadosAgregados.objects.get_or_create(
                id_cliente=id_cliente,
                id_equipamento=id_equipamento,
                periodo_inicio=periodo_inicio,
                defaults={
                    'periodo_fim': periodo_fim,
                    'corrente_descascadores_media': sum(valores) / len(valores),
                    'corrente_descascadores_max': max(valores),
                    'corrente_descascadores_min': min(valores),
                    'corrente_descascadores_ultima': grupo_registros[-1].corrente,
                    'registros_contagem': len(grupo_registros),
                }
            )
            
            if not created:
                agregado.corrente_descascadores_media = sum(valores) / len(valores)
                agregado.corrente_descascadores_max = max(valores)
                agregado.corrente_descascadores_min = min(valores)
                agregado.corrente_descascadores_ultima = grupo_registros[-1].corrente
                agregado.save()
        
        CorrenteDescascadores.objects.filter(agregado=False).update(agregado=True)

    def agregar_corrente_polidores_orm(self, intervalo):
        """Agrega dados de corrente dos polidores usando Django ORM"""
        registros = CorrentePolidores.objects.filter(agregado=False)
        
        grupos = {}
        for registro in registros:
            periodo_inicio = self._format_periodo(registro.timestamp, intervalo)
            periodo_fim = periodo_inicio + intervalo
            chave = (registro.id_cliente, registro.id_equipamento, periodo_inicio)
            
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append(registro)
        
        for (id_cliente, id_equipamento, periodo_inicio), grupo_registros in grupos.items():
            periodo_fim = periodo_inicio + intervalo
            valores = [r.corrente for r in grupo_registros]
            
            agregado, created = DadosAgregados.objects.get_or_create(
                id_cliente=id_cliente,
                id_equipamento=id_equipamento,
                periodo_inicio=periodo_inicio,
                defaults={
                    'periodo_fim': periodo_fim,
                    'corrente_polidores_media': sum(valores) / len(valores),
                    'corrente_polidores_max': max(valores),
                    'corrente_polidores_min': min(valores),
                    'corrente_polidores_ultima': grupo_registros[-1].corrente,
                    'registros_contagem': len(grupo_registros),
                }
            )
            
            if not created:
                agregado.corrente_polidores_media = sum(valores) / len(valores)
                agregado.corrente_polidores_max = max(valores)
                agregado.corrente_polidores_min = min(valores)
                agregado.corrente_polidores_ultima = grupo_registros[-1].corrente
                agregado.save()
        
        CorrentePolidores.objects.filter(agregado=False).update(agregado=True)

    def agregar_temperaturas_orm(self, intervalo):
        """Agrega dados de temperatura usando Django ORM"""
        registros = Temperatura.objects.filter(agregado=False)
        
        grupos = {}
        for registro in registros:
            periodo_inicio = self._format_periodo(registro.timestamp, intervalo)
            periodo_fim = periodo_inicio + intervalo
            chave = (registro.id_cliente, registro.id_equipamento, periodo_inicio)
            
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append(registro)
        
        for (id_cliente, id_equipamento, periodo_inicio), grupo_registros in grupos.items():
            periodo_fim = periodo_inicio + intervalo
            valores = [r.temperatura for r in grupo_registros]
            
            agregado, created = DadosAgregados.objects.get_or_create(
                id_cliente=id_cliente,
                id_equipamento=id_equipamento,
                periodo_inicio=periodo_inicio,
                defaults={
                    'periodo_fim': periodo_fim,
                    'temperatura_media': sum(valores) / len(valores),
                    'temperatura_max': max(valores),
                    'temperatura_min': min(valores),
                    'temperatura_ultima': grupo_registros[-1].temperatura,
                    'registros_contagem': len(grupo_registros),
                }
            )
            
            if not created:
                agregado.temperatura_media = sum(valores) / len(valores)
                agregado.temperatura_max = max(valores)
                agregado.temperatura_min = min(valores)
                agregado.temperatura_ultima = grupo_registros[-1].temperatura
                agregado.save()
        
        Temperatura.objects.filter(agregado=False).update(agregado=True)

    def agregar_umidades_orm(self, intervalo):
        """Agrega dados de umidade usando Django ORM"""
        registros = Umidade.objects.filter(agregado=False)
        
        grupos = {}
        for registro in registros:
            periodo_inicio = self._format_periodo(registro.timestamp, intervalo)
            periodo_fim = periodo_inicio + intervalo
            chave = (registro.id_cliente, registro.id_equipamento, periodo_inicio)
            
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append(registro)
        
        for (id_cliente, id_equipamento, periodo_inicio), grupo_registros in grupos.items():
            periodo_fim = periodo_inicio + intervalo
            valores = [r.umidade for r in grupo_registros]
            
            agregado, created = DadosAgregados.objects.get_or_create(
                id_cliente=id_cliente,
                id_equipamento=id_equipamento,
                periodo_inicio=periodo_inicio,
                defaults={
                    'periodo_fim': periodo_fim,
                    'umidade_media': sum(valores) / len(valores),
                    'umidade_max': max(valores),
                    'umidade_min': min(valores),
                    'umidade_ultima': grupo_registros[-1].umidade,
                    'registros_contagem': len(grupo_registros),
                }
            )
            
            if not created:
                agregado.umidade_media = sum(valores) / len(valores)
                agregado.umidade_max = max(valores)
                agregado.umidade_min = min(valores)
                agregado.umidade_ultima = grupo_registros[-1].umidade
                agregado.save()
        
        Umidade.objects.filter(agregado=False).update(agregado=True)

    def agregar_grandezas_eletricas_orm(self, intervalo):
        """Agrega dados de grandezas elétricas usando Django ORM"""
        registros = GrandezaEletrica.objects.filter(agregado=False)
        
        grupos = {}
        for registro in registros:
            periodo_inicio = self._format_periodo(registro.timestamp, intervalo)
            periodo_fim = periodo_inicio + intervalo
            chave = (registro.id_cliente, registro.id_equipamento, periodo_inicio)
            
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append(registro)
        
        for (id_cliente, id_equipamento, periodo_inicio), grupo_registros in grupos.items():
            periodo_fim = periodo_inicio + intervalo
            
            # Calcula médias, máximos e mínimos
            campos = ['tensao_r', 'tensao_s', 'tensao_t', 'corrente_r', 'corrente_s', 'corrente_t',
                     'potencia_ativa', 'potencia_reativa', 'fator_potencia']
            
            agregado, created = DadosAgregados.objects.get_or_create(
                id_cliente=id_cliente,
                id_equipamento=id_equipamento,
                periodo_inicio=periodo_inicio,
                defaults={
                    'periodo_fim': periodo_fim,
                    'registros_contagem': len(grupo_registros),
                }
            )
            
            # Processa cada campo
            for campo in campos:
                valores = [getattr(r, campo) for r in grupo_registros if getattr(r, campo) is not None]
                if valores:
                    setattr(agregado, f'{campo}_media', sum(valores) / len(valores))
                    setattr(agregado, f'{campo}_max', max(valores))
                    setattr(agregado, f'{campo}_min', min(valores))
                    setattr(agregado, f'{campo}_ultima', getattr(grupo_registros[-1], campo))
            
            agregado.save()
        
        GrandezaEletrica.objects.filter(agregado=False).update(agregado=True)
