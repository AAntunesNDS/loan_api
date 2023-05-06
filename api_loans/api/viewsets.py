import math

from rest_framework import viewsets
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from api_loans.api.serializers import EmprestimoSerializer, PagamentoSerializer
from ..models import Emprestimo, Pagamento

from datetime import datetime, timezone


class EmprestimoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmprestimoSerializer
    queryset = Emprestimo.objects.all()

    @action(methods=["GET"], detail=True, url_path="saldo-devedor")
    def saldo_devedor(self, request, pk=None):
        emprestimo = self.get_object()

        valor_pago = (
            Pagamento.objects.filter(id_emprestimo=pk).aggregate(
                Sum("valor_pagamento")
            )["valor_pagamento__sum"]
            or 0
        )

        valor_nominal = (
            emprestimo.valor_nominal
        )  # valor_devido inicia com o valor_nominal
        #   se valor = 0 usarei data solicitação do emprestimo
        # para calcular o juros compostos
        #   se nao, pego a data do ultimo pagamento com valor > 0
        if valor_pago == 0:
            dias_do_ultimo_pagamento = (
                datetime.now(timezone.utc)
                - emprestimo.data_solicitacao.replace(tzinfo=timezone.utc)
            ).days
            qtd_meses = math.floor(dias_do_ultimo_pagamento / 30)
            for mes in range(qtd_meses):
                valor_devido = (
                    emprestimo.taxa_de_juros / 100
                ) * valor_nominal + valor_nominal
                valor_nominal = valor_devido

        else:
            ultimo_pagamento = Pagamento.objects.filter(
                id_emprestimo=pk, valor_pagamento__gt=0
            ).latest("data_pagamento")
            dias_do_ultimo_pagamento = (
                datetime.now(timezone.utc)
                - ultimo_pagamento.data_pagamento.replace(tzinfo=timezone.utc)
            ).days
            qtd_meses = math.floor(dias_do_ultimo_pagamento / 30)
            # se um usuario tomou um emprestimo e faz o pagamento no mesmo mes, nao tem juros
            # essa logica pode ser alterada
            if qtd_meses == 0:
                valor_devido = valor_nominal - ultimo_pagamento
            for mes in range(qtd_meses):
                valor_devido = (
                    emprestimo.taxa_de_juros / 100
                ) * valor_nominal + valor_nominal
                valor_nominal = valor_devido

            valor_devido -= valor_pago

        emprestimo.valor_devido = valor_devido  # atualiza o atributo valor_devido
        emprestimo.save()  # salva o objeto atualizado

        return Response({"saldo_devedor": emprestimo.valor_devido})


class PagamentoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PagamentoSerializer
    queryset = Pagamento.objects.all()
