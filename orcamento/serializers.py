from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers

from orcamento.models import *


class ReceitaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Receita
        fields = ['id', 'descricao', 'valor', 'data']
        read_only_fields = ['id']

    def _descricao_duplicada_no_mes(self, descricao, data):
        exists = Receita.objects.filter(
            data__month=data.month,
            descricao__icontains=descricao,
        ).exists()

        return exists

    def validate(self, attrs):
        descricao = attrs.get('descricao')
        data = attrs.get('data')
        
        if self._descricao_duplicada_no_mes(descricao, data):
            raise serializers.ValidationError({'descricao': 'Já existe uma descrição para esse mês.'})

        super_validade = super().validate(attrs)
        return super_validade

    def create(self, validated_data):
        data = validated_data.get('data')
        new_valor = validated_data.get('valor')

        resumo_mes = ResumoMes.objects.filter(data__month=data.month)

        if resumo_mes.exists():
            res = resumo_mes.first()
            res.receita_total += new_valor
            res.save()
        else:
            ResumoMes.objects.create(data=data, receita_total=new_valor)

        return super().create(validated_data)
    
   
        

