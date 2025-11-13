from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings
from leituras.models import (
    CorrenteBrunidores,
    CorrenteDescascadores,
    CorrentePolidores,
    Temperatura,
    Umidade,
    GrandezaEletrica,
    DadosAgregados
)


class Command(BaseCommand):
    help = 'Conta o número de registros em cada tabela do banco de dados'

    def handle(self, *args, **options):
        # Obtém informações do banco configurado
        db_config = settings.DATABASES['default']
        db_name = db_config.get('NAME', 'N/A')
        db_engine = db_config.get('ENGINE', 'N/A')
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Contagem de Registros ==='))
        self.stdout.write(self.style.SUCCESS(f'Banco de Dados: {db_name}'))
        self.stdout.write(self.style.SUCCESS(f'Engine: {db_engine}\n'))
        
        # Tabelas do Django (sistema)
        django_tables = [
            'django_migrations',
            'django_content_type',
            'auth_permission',
            'auth_group',
            'auth_user',
            'django_session',
            'django_admin_log',
        ]
        
        # Tabelas da aplicação
        app_tables = [
            ('corrente_brunidores', CorrenteBrunidores),
            ('corrente_descascadores', CorrenteDescascadores),
            ('corrente_polidores', CorrentePolidores),
            ('temperaturas', Temperatura),
            ('umidades', Umidade),
            ('grandezas_eletricas', GrandezaEletrica),
            ('dados_agregados', DadosAgregados),
        ]
        
        # Conta registros nas tabelas da aplicação usando Django ORM
        self.stdout.write(self.style.WARNING('--- Tabelas da Aplicação ---'))
        total_app = 0
        for table_name, model in app_tables:
            try:
                count = model.objects.count()
                total_app += count
                self.stdout.write(f'{table_name:.<40} {count:>10,} registros')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'{table_name:.<40} ERRO: {str(e)}'))
        
        self.stdout.write(f'\n{"TOTAL (Aplicação)":.<40} {total_app:>10,} registros\n')
        
        # Conta registros nas tabelas do Django usando SQL direto
        self.stdout.write(self.style.WARNING('--- Tabelas do Sistema (Django) ---'))
        total_django = 0
        
        with connection.cursor() as cursor:
            for table in django_tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    total_django += count
                    self.stdout.write(f'{table:.<40} {count:>10,} registros')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'{table:.<40} ERRO: {str(e)}'))
        
        self.stdout.write(f'\n{"TOTAL (Sistema)":.<40} {total_django:>10,} registros\n')
        
        # Lista todas as tabelas do banco
        self.stdout.write(self.style.WARNING('--- Todas as Tabelas do Banco ---'))
        with connection.cursor() as cursor:
            # Para MySQL
            if 'mysql' in connection.vendor:
                cursor.execute("""
                    SELECT TABLE_NAME, TABLE_ROWS 
                    FROM information_schema.TABLES 
                    WHERE TABLE_SCHEMA = DATABASE()
                    ORDER BY TABLE_NAME
                """)
                tables_info = cursor.fetchall()
                total_all = 0
                for table_name, table_rows in tables_info:
                    # TABLE_ROWS pode ser aproximado, então vamos contar exatamente
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                        exact_count = cursor.fetchone()[0]
                        total_all += exact_count
                        self.stdout.write(f'{table_name:.<40} {exact_count:>10,} registros')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'{table_name:.<40} ERRO: {str(e)}'))
                
                self.stdout.write(f'\n{"TOTAL GERAL":.<40} {total_all:>10,} registros\n')
            else:
                # Para SQLite
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
                tables = cursor.fetchall()
                total_all = 0
                for (table_name,) in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                        count = cursor.fetchone()[0]
                        total_all += count
                        self.stdout.write(f'{table_name:.<40} {count:>10,} registros')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'{table_name:.<40} ERRO: {str(e)}'))
                
                self.stdout.write(f'\n{"TOTAL GERAL":.<40} {total_all:>10,} registros\n')
        
        self.stdout.write(self.style.SUCCESS('\n=== Contagem concluída! ===\n'))

