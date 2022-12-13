from rest_framework import viewsets

from orcamento.models import *
from orcamento.serializers import *


class ReceitaViewSet(viewsets.ModelViewSet):
    serializer_class = ReceitaSerializer
    queryset = Receita.objects.all()
    