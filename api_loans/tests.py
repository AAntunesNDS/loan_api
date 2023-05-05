from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from .models import Emprestimo, Pagamento
from uuid import UUID

from rest_framework.test import APIClient
from api_loans.models import Emprestimo, Pagamento

from django.contrib.auth.models import User
from datetime import datetime


class TestEmprestimoViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser")

    def test_listar_emprestimos(self):
        Emprestimo.objects.create(
            valor_nominal=1000,
            taxa_de_juros=0.1,
            endereco_ip="127.0.0.1",
            data_solicitacao="2022-01-01T00:00:00Z",
            banco="Banco A",
            cliente=self.user,
        )
        Emprestimo.objects.create(
            valor_nominal=2000,
            taxa_de_juros=0.2,
            endereco_ip="127.0.0.2",
            data_solicitacao="2022-01-02T00:00:00Z",
            banco="Banco B",
            cliente=self.user,
        )

        response = self.client.get("/loans/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_criar_emprestimo(self):
        data = {
            "valor_nominal": 1000,
            "taxa_de_juros": 0.1,
            "endereco_ip": "127.0.0.1",
            "data_solicitacao": "2022-01-01T00:00:00Z",
            "banco": "Banco A",
        }

        response = self.client.post("/loans/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Emprestimo.objects.count(), 1)
        emprestimo = Emprestimo.objects.first()
        self.assertEqual(emprestimo.valor_nominal, data["valor_nominal"])


class TestPagamentoViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser")
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=1000,
            taxa_de_juros=0.1,
            endereco_ip="127.0.0.1",
            data_solicitacao="2022-01-01T00:00:00Z",
            banco="Banco A",
            cliente=self.user,
        )

    def test_listar_pagamentos(self):
        Pagamento.objects.create(
            id_emprestimo=self.emprestimo,
            data_pagamento="2022-02-01T00:00:00Z",
            valor_pagamento=500,
        )
        Pagamento.objects.create(
            id_emprestimo=self.emprestimo,
            data_pagamento="2022-03-01T00:00:00Z",
            valor_pagamento=600,
        )

        response = self.client.get(f"/payment/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_criar_pagamento(self):
        data = {
            "id_emprestimo": self.emprestimo.id_emprestimo,
            "data_pagamento": "2022-02-01T00:00:00Z",
            "valor_pagamento": 500,
        }

        response = self.client.post(f"/payment/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Pagamento.objects.count(), 1)
        pagamento = Pagamento.objects.first()
        self.assertEqual(pagamento.valor_pagamento, data["valor_pagamento"])


class EmprestimoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testuser", password="testpass")
        cls.emprestimo = Emprestimo.objects.create(
            valor_nominal=1000.00,
            taxa_de_juros=0.05,
            endereco_ip="127.0.0.1",
            data_solicitacao=datetime.now(),
            banco="Banco X",
            cliente=cls.user,
        )

    def test_valor_nominal_label(self):
        emprestimo = Emprestimo.objects.get(id_emprestimo=self.emprestimo.id_emprestimo)
        field_label = emprestimo._meta.get_field("valor_nominal").verbose_name
        self.assertEqual(field_label, "valor nominal")

    def test_cliente_label(self):
        emprestimo = Emprestimo.objects.get(id_emprestimo=self.emprestimo.id_emprestimo)
        field_label = emprestimo._meta.get_field("cliente").verbose_name
        self.assertEqual(field_label, "cliente")

    def test_valor_nominal_max_digits(self):
        emprestimo = Emprestimo.objects.get(id_emprestimo=self.emprestimo.id_emprestimo)
        max_digits = emprestimo._meta.get_field("valor_nominal").max_digits
        self.assertEqual(max_digits, 10)

    def test_taxa_de_juros_max_digits(self):
        emprestimo = Emprestimo.objects.get(id_emprestimo=self.emprestimo.id_emprestimo)
        max_digits = emprestimo._meta.get_field("taxa_de_juros").max_digits
        self.assertEqual(max_digits, 2)

    def test_endereco_ip_max_length(self):
        emprestimo = Emprestimo.objects.get(id_emprestimo=self.emprestimo.id_emprestimo)
        max_length = emprestimo._meta.get_field("endereco_ip").max_length
        self.assertEqual(max_length, 20)

    def test_cliente_null(self):
        emprestimo = Emprestimo.objects.create(
            valor_nominal=2000.00,
            taxa_de_juros=0.05,
            endereco_ip="127.0.0.1",
            data_solicitacao=datetime.now(),
            banco="Banco Y",
            cliente=None,
        )
        self.assertIsNone(emprestimo.cliente)


class PagamentoTestCase(TestCase):
    def setUp(self):
        # Criar um usuário para teste
        self.user = User.objects.create(username="testuser")

        # Criar um empréstimo para teste
        self.emprestimo = Emprestimo.objects.create(
            valor_nominal=Decimal("1000.00"),
            taxa_de_juros=Decimal("0.05"),
            endereco_ip="127.0.0.1",
            data_solicitacao=datetime.now(),
            banco="Banco de Teste",
            cliente=self.user,
            created_at=datetime.now().date(),
        )

        # Criar um pagamento para teste
        self.pagamento = Pagamento.objects.create(
            id_emprestimo=self.emprestimo,
            data_pagamento=datetime.now(),
            valor_pagamento=Decimal("500.00"),
            cliente=self.user,
            created_at=datetime.now().date(),
        )

    def test_id_pagamento_deve_ser_um_uuid(self):
        self.assertIsNotNone(self.pagamento.id_pagamento)
        self.assertIsInstance(self.pagamento.id_pagamento, UUID)

    def test_id_emprestimo_deve_ser_do_tipo_Emprestimo(self):
        self.assertIsInstance(self.pagamento.id_emprestimo, Emprestimo)

    def test_data_pagamento_deve_ser_do_tipo_datetime(self):
        self.assertIsInstance(self.pagamento.data_pagamento, datetime)

    def test_valor_pagamento_deve_ser_do_tipo_decimal(self):
        self.assertIsInstance(self.pagamento.valor_pagamento, Decimal)

    def test_cliente_deve_ser_do_tipo_User(self):
        self.assertIsInstance(self.pagamento.cliente, User)

    def test_str_deve_retornar_string_formatada(self):
        self.assertEqual(
            str(self.pagamento), f"Pagamento {self.pagamento.id_pagamento}"
        )

    # def test_valor_restante_deve_retornar_valor_correto(self):
    # valor_restante = self.pagamento.valor_restante()
    # self.assertEqual(valor_restante, Decimal('500.00'))

    # def test_valor_restante_deve_retornar_zero_quando_pagamento_igual_ao_valor_do_emprestimo(self):
    #    pagamento = Pagamento.objects.create(
    #        id_emprestimo=self.emprestimo,
    #        data_pagamento=datetime.now(),
    #        valor_pagamento=Decimal('1000.00'),
    #        cliente=self.user,
    #        created_at=datetime.now().date()
    #    )
    #    valor_restante = pagamento.valor_restante()
    #    self.assertEqual(valor_restante, Decimal('0.00'))
