from rest_framework import viewsets
from api.api.serializers import EmprestimoSerializer
from api.models import Emprestimo


class EmprestimoViewSet(viewsets.ModelViewSet):
    serializer_class = EmprestimoSerializer
    queryset = Emprestimo.objects.all()