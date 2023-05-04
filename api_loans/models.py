from django.db import models
from uuid import uuid4


# Create your models here.

class Emprestimo(models.Model):
    id_emprestimo = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    valor_nominal = models.DecimalField(max_digits=10, decimal_places=2)
    taxa_de_juros = models.DecimalField(max_digits=2, decimal_places=2)
    endereco_ip = models.CharField(max_length=20)
    data_solicitacao = models.DateTimeField()
    banco = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)


class Pagamento(models.Model):
    id_pagamento = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id_emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)
    data_pagamento = models.DateTimeField()
    valor_pagamento = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateField(auto_now_add=True)

    