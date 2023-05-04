from rest_framework import viewsets
from api_loans.api.serializers import EmprestimoSerializer, PagamentoSerializer
from ..models import Emprestimo, Pagamento


class EmprestimoViewSet(viewsets.ModelViewSet):
    serializer_class = EmprestimoSerializer
    queryset = Emprestimo.objects.all()

class PagamentoViewSet(viewsets.ModelViewSet):
    serializer_class = PagamentoSerializer
    queryset = Pagamento.objects.all()