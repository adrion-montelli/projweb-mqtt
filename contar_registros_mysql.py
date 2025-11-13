"""
Script para contar registros nas tabelas do banco db_mqtt_teste
Execute: python contar_registros_mysql.py
"""
import pymysql
from getpass import getpass

# Configurações do banco de dados
# Você pode modificar estas configurações ou usar variáveis de ambiente
import os

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '10.1.1.243'),  # Servidor remoto
    'port': int(os.environ.get('DB_PORT', '3306')),
    'user': os.environ.get('DB_USERNAME', 'external'),
    'password': os.environ.get('DB_PASSWORD', 'SenhaExt123'),
    'database': os.environ.get('DB_DATABASE', 'db_mqtt_teste'),
    'charset': 'utf8mb4'
}

def contar_registros():
    """Conta registros em todas as tabelas do banco"""
    
    # Tenta obter senha de variável de ambiente
    import os
    if not DB_CONFIG['password']:
        DB_CONFIG['password'] = os.environ.get('DB_PASSWORD', '')
    
    # Se ainda não tiver senha, tenta sem senha primeiro
    if not DB_CONFIG['password']:
        DB_CONFIG['password'] = None
    
    try:
        # Conecta ao banco
        connection = pymysql.connect(**DB_CONFIG)
        
        print(f'\n{"="*60}')
        print(f'Contagem de Registros - Banco: {DB_CONFIG["database"]}')
        print(f'{"="*60}\n')
        
        with connection.cursor() as cursor:
            # Lista todas as tabelas do banco
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = %s
                ORDER BY TABLE_NAME
            """, (DB_CONFIG['database'],))
            
            tables = cursor.fetchall()
            
            if not tables:
                print(f'Nenhuma tabela encontrada no banco {DB_CONFIG["database"]}')
                return
            
            # Tabelas da aplicação (principais)
            app_tables = [
                'corrente_brunidores',
                'corrente_descascadores',
                'corrente_polidores',
                'temperaturas',
                'umidades',
                'grandezas_eletricas',
                'dados_agregados',
            ]
            
            # Tabelas do Django
            django_tables = [
                'django_migrations',
                'django_content_type',
                'auth_permission',
                'auth_group',
                'auth_user',
                'django_session',
                'django_admin_log',
            ]
            
            print('--- Tabelas da Aplicação ---')
            total_app = 0
            for table_name, in tables:
                if table_name in app_tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                        count = cursor.fetchone()[0]
                        total_app += count
                        print(f'{table_name:.<45} {count:>12,} registros')
                    except Exception as e:
                        print(f'{table_name:.<45} ERRO: {str(e)}')
            
            print(f'\n{"TOTAL (Aplicação)":.<45} {total_app:>12,} registros\n')
            
            print('--- Tabelas do Sistema (Django) ---')
            total_django = 0
            for table_name, in tables:
                if table_name in django_tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                        count = cursor.fetchone()[0]
                        total_django += count
                        print(f'{table_name:.<45} {count:>12,} registros')
                    except Exception as e:
                        print(f'{table_name:.<45} ERRO: {str(e)}')
            
            print(f'\n{"TOTAL (Sistema)":.<45} {total_django:>12,} registros\n')
            
            print('--- Todas as Tabelas do Banco ---')
            total_all = 0
            for table_name, in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                    count = cursor.fetchone()[0]
                    total_all += count
                    print(f'{table_name:.<45} {count:>12,} registros')
                except Exception as e:
                    print(f'{table_name:.<45} ERRO: {str(e)}')
            
            print(f'\n{"TOTAL GERAL":.<45} {total_all:>12,} registros\n')
            
            # Estatísticas adicionais
            print('--- Estatísticas Adicionais ---')
            
            # Conta registros agregados vs não agregados
            for table in ['corrente_brunidores', 'corrente_descascadores', 'corrente_polidores', 
                         'temperaturas', 'umidades', 'grandezas_eletricas']:
                try:
                    cursor.execute(f"""
                        SELECT 
                            COUNT(*) as total,
                            SUM(CASE WHEN agregado = 1 THEN 1 ELSE 0 END) as agregados,
                            SUM(CASE WHEN agregado = 0 THEN 1 ELSE 0 END) as nao_agregados
                        FROM `{table}`
                    """)
                    result = cursor.fetchone()
                    if result and result[0] > 0:
                        total, agregados, nao_agregados = result
                        print(f'{table}:')
                        print(f'  Total: {total:,} | Agregados: {agregados:,} | Não agregados: {nao_agregados:,}')
                except Exception as e:
                    pass
            
            print(f'\n{"="*60}')
            print('Contagem concluída!')
            print(f'{"="*60}\n')
        
        connection.close()
        
    except pymysql.Error as e:
        print(f'\nERRO ao conectar ao banco de dados: {e}')
        print(f'\nVerifique:')
        print(f'  - O MySQL está rodando?')
        print(f'  - O banco {DB_CONFIG["database"]} existe?')
        print(f'  - As credenciais estão corretas?')
        print(f'  - O usuário tem permissão para acessar o banco?')
    except Exception as e:
        print(f'\nERRO: {e}')

if __name__ == '__main__':
    contar_registros()

