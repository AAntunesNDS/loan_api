from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from .models import Emprestimo, Pagamento
from uuid import uuid4
from django.test import TestCase
from rest_framework.test import APIClient
from api_loans.models import Emprestimo, Pagamento


class TestEmprestimoViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_listar_emprestimos(self):
        Emprestimo.objects.create(valor_nominal=1000, taxa_de_juros=0.1, endereco_ip='127.0.0.1', 
            data_solicitacao='2022-01-01T00:00:00Z', banco='Banco A', cliente='Fulano')
        Emprestimo.objects.create(valor_nominal=2000, taxa_de_juros=0.2, endereco_ip='127.0.0.2', 
            data_solicitacao='2022-01-02T00:00:00Z', banco='Banco B', cliente='Ciclano')

        response = self.client.get('/loans/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_criar_emprestimo(self):
        data = {
            'valor_nominal': 1000,
            'taxa_de_juros': 0.1,
            'endereco_ip': '127.0.0.1',
            'data_solicitacao': '2022-01-01T00:00:00Z',
            'banco': 'Banco A',
            'cliente': 'Fulano'
        }

        response = self.client.post('/loans/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Emprestimo.objects.count(), 1)
        emprestimo = Emprestimo.objects.first()
        self.assertEqual(emprestimo.valor_nominal, data['valor_nominal'])

class TestPagamentoViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.emprestimo = Emprestimo.objects.create(valor_nominal=1000, taxa_de_juros=0.1, endereco_ip='127.0.0.1', 
            data_solicitacao='2022-01-01T00:00:00Z', banco='Banco A', cliente='Fulano')

    def test_listar_pagamentos(self):
        Pagamento.objects.create(id_emprestimo=self.emprestimo, data_pagamento='2022-02-01T00:00:00Z', valor_pagamento=500)
        Pagamento.objects.create(id_emprestimo=self.emprestimo, data_pagamento='2022-03-01T00:00:00Z', valor_pagamento=600)

        response = self.client.get(f'/payment/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_criar_pagamento(self):
        data = {
            'id_emprestimo': self.emprestimo.id_emprestimo,
            'data_pagamento': '2022-02-01T00:00:00Z',
            'valor_pagamento': 500,
        }

        response = self.client.post(f'/payment/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pagamento.objects.count(), 1)
        pagamento = Pagamento.objects.first()
        self.assertEqual(pagamento.valor_pagamento, data['valor_pagamento'])



class EmprestimoTestCase(TestCase):
    def setUp(self):
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal('1000.00'),
            taxa_de_juros=Decimal('0.05'),
            endereco_ip='127.0.0.1',
            data_solicitacao=timezone.now(),
            banco='Meu banco',
            cliente='João da Silva'
        )

    def test_emprestimo_criado_com_sucesso(self):
        emprestimo = Emprestimo.objects.get(pk=self.emprestimo.pk)
        self.assertEqual(emprestimo.valor_nominal, Decimal('1000.00'))
        self.assertEqual(emprestimo.taxa_de_juros, Decimal('0.05'))
        self.assertEqual(emprestimo.endereco_ip, '127.0.0.1')
        self.assertEqual(emprestimo.banco, 'Meu banco')
        self.assertEqual(emprestimo.cliente, 'João da Silva')

class PagamentoTestCase(TestCase):
    def setUp(self):
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal('1000.00'),
            taxa_de_juros=Decimal('0.05'),
            endereco_ip='127.0.0.1',
            data_solicitacao=timezone.now(),
            banco='Meu banco',
            cliente='João da Silva'
        )
        self.pagamento = Pagamento.objects.create(
            id_emprestimo=self.emprestimo,
            data_pagamento=timezone.now(),
            valor_pagamento=Decimal('1050.00')
        )

    def test_pagamento_criado_com_sucesso(self):
        pagamento = Pagamento.objects.get(pk=self.pagamento.pk)
        self.assertEqual(pagamento.id_emprestimo, self.emprestimo)
        self.assertEqual(pagamento.valor_pagamento, Decimal('1050.00'))
