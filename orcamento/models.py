
from django.contrib.auth import get_user_model
from django.db import models


class Receita(models.Model):
    descricao = models.CharField(max_length=255, blank=True, null=True)
    valor = models.FloatField()
    data = models.DateField()
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = 'Receitas'


class Despesa(models.Model):
    CODIGO_DESPESA =(
        ('F', 'Despesa fixa'),
        ('E', 'Despesa eventual')
    )
    descricao = models.CharField(max_length=255, blank=True, null=True)
    valor = models.FloatField()
    data = models.DateField()
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    codigo_despesa = models.CharField(max_length=1, choices=CODIGO_DESPESA)

    class Meta:
        db_table = 'Despesas'

class ResumoMes(models.Model):
    """Tabela que é atualizada toda vez que uma receita e despesa são cadastradas."""
    data = models.DateField(primary_key=True)
    receita_total = models.FloatField(null=True, blank=True)
    despesa_fixa_total = models.FloatField(null=True, blank=True)
    despesa_eventual_total = models.FloatField(null=True, blank=True)
    saldo_final = models.FloatField()
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = 'Resumo do Mes'