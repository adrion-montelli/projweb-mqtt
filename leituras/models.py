from django.db import models


class CorrenteBrunidores(models.Model):
    id_cliente = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    corrente = models.DecimalField(max_digits=10, decimal_places=2)
    agregado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'corrente_brunidores'
        indexes = [
            models.Index(fields=['id_cliente', 'id_equipamento', 'timestamp']),
        ]


class CorrenteDescascadores(models.Model):
    id_cliente = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    corrente = models.DecimalField(max_digits=10, decimal_places=2)
    agregado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'corrente_descascadores'
        indexes = [
            models.Index(fields=['id_cliente', 'id_equipamento', 'timestamp']),
        ]


class CorrentePolidores(models.Model):
    id_cliente = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    corrente = models.DecimalField(max_digits=10, decimal_places=2)
    agregado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'corrente_polidores'
        indexes = [
            models.Index(fields=['id_cliente', 'id_equipamento', 'timestamp']),
        ]


class Temperatura(models.Model):
    id_cliente = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    temperatura = models.DecimalField(max_digits=10, decimal_places=2)
    agregado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'temperaturas'
        indexes = [
            models.Index(fields=['id_cliente', 'id_equipamento', 'timestamp']),
        ]


class Umidade(models.Model):
    id_cliente = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    umidade = models.DecimalField(max_digits=10, decimal_places=2)
    agregado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'umidades'
        indexes = [
            models.Index(fields=['id_cliente', 'id_equipamento', 'timestamp']),
        ]


class GrandezaEletrica(models.Model):
    id_cliente = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    tensao_r = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_s = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_t = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_r = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_s = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_t = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_ativa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_reativa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fator_potencia = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    agregado = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grandezas_eletricas'
        indexes = [
            models.Index(fields=['id_cliente', 'id_equipamento', 'timestamp']),
        ]


class DadosAgregados(models.Model):
    id_cliente = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    periodo_inicio = models.DateTimeField()
    periodo_fim = models.DateTimeField()

    # Corrente Brunidores
    corrente_brunidores_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_brunidores_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_brunidores_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_brunidores_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Corrente Descascadores
    corrente_descascadores_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_descascadores_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_descascadores_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_descascadores_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Corrente Polidores
    corrente_polidores_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_polidores_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_polidores_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_polidores_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Temperaturas
    temperatura_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temperatura_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temperatura_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    temperatura_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Umidades
    umidade_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    umidade_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    umidade_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    umidade_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Tensão R
    tensao_r_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_r_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_r_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_r_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Tensão S
    tensao_s_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_s_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_s_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_s_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Tensão T
    tensao_t_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_t_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_t_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tensao_t_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Corrente R
    corrente_r_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_r_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_r_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_r_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Corrente S
    corrente_s_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_s_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_s_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_s_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Corrente T
    corrente_t_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_t_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_t_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    corrente_t_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Potência Ativa
    potencia_ativa_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_ativa_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_ativa_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_ativa_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Potência Reativa
    potencia_reativa_media = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_reativa_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_reativa_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    potencia_reativa_ultima = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Grandezas elétricas - Fator de Potência
    fator_potencia_media = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    fator_potencia_max = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    fator_potencia_min = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    fator_potencia_ultima = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    registros_contagem = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dados_agregados'
        unique_together = [['id_cliente', 'id_equipamento', 'periodo_inicio']]
        indexes = [
            models.Index(fields=['id_cliente']),
            models.Index(fields=['id_equipamento']),
            models.Index(fields=['periodo_fim']),
        ]
