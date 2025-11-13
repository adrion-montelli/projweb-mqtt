from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Testa a conexão com o banco de dados configurado'

    def handle(self, *args, **options):
        db_config = settings.DATABASES['default']
        
        self.stdout.write(self.style.SUCCESS('\n=== Teste de Conexão com Banco de Dados ===\n'))
        self.stdout.write(f'Engine: {db_config.get("ENGINE", "N/A")}')
        self.stdout.write(f'Host: {db_config.get("HOST", "N/A")}')
        self.stdout.write(f'Port: {db_config.get("PORT", "N/A")}')
        self.stdout.write(f'Database: {db_config.get("NAME", "N/A")}')
        self.stdout.write(f'User: {db_config.get("USER", "N/A")}')
        self.stdout.write('')
        
        try:
            # Tenta conectar
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
            self.stdout.write(self.style.SUCCESS('✓ Conexão estabelecida com sucesso!'))
            
            # Obtém o nome do banco das configurações
            db_name = db_config.get('NAME', 'N/A')
            self.stdout.write(self.style.SUCCESS(f'✓ Banco conectado: {db_name}'))
            
            # Conta tabelas
            if 'mysql' in connection.vendor:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM information_schema.TABLES 
                        WHERE TABLE_SCHEMA = %s
                    """, [db_name])
                    table_count = cursor.fetchone()[0]
                    self.stdout.write(self.style.SUCCESS(f'✓ Total de tabelas: {table_count}'))
            elif 'sqlite' in connection.vendor:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    self.stdout.write(self.style.SUCCESS(f'✓ Total de tabelas: {len(tables)}'))
            
            self.stdout.write(self.style.SUCCESS('\n=== Conexão OK! ===\n'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ ERRO ao conectar: {e}'))
            self.stdout.write(self.style.WARNING('\nVerifique:'))
            self.stdout.write('  - As variáveis de ambiente estão configuradas?')
            self.stdout.write('  - O servidor MySQL está acessível?')
            self.stdout.write('  - As credenciais estão corretas?')
            self.stdout.write('')

