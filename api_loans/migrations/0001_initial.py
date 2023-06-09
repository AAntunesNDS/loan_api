# Generated by Django 4.2 on 2023-05-04 01:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Emprestimo",
            fields=[
                (
                    "id_emprestimo",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("valor_nominal", models.DecimalField(decimal_places=2, max_digits=10)),
                ("taxa_de_juros", models.DecimalField(decimal_places=2, max_digits=2)),
                ("endereco_ip", models.CharField(max_length=20)),
                ("data_solicitacao", models.DateTimeField()),
                ("banco", models.CharField(max_length=255)),
                ("cliente", models.CharField(max_length=255)),
                ("created_at", models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Pagamento",
            fields=[
                (
                    "id_pagamento",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("data_pagamento", models.DateTimeField()),
                (
                    "valor_pagamento",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("create_at", models.DateField(auto_now_add=True)),
                (
                    "id_emprestimo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api_loans.emprestimo",
                    ),
                ),
            ],
        ),
    ]
