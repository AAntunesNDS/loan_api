from django.db import models
from uuid import uuid4


# Create your models here.

class Emprestimo(models.Model):
    id_emprestimo = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    valor_nominal = models.CharField(max_length=255)
    taxa_de_juros = models.CharField(max_length=255)
    endereco_ip = models.IntegerField()
    data_solicitacao = models.CharField(max_length=50)
    banco = models.IntegerField()
    cliente = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)


class Pagamento(models.Model):
    id_pagamento = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id_emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)
    data_pagamento = models.CharField(max_length=50)
    valor_pagamento = models.IntegerField()
    create_at = models.DateField(auto_now_add=True)