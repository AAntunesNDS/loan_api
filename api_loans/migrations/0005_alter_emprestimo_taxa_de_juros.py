# Generated by Django 4.2 on 2023-05-06 15:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_loans", "0004_rename_create_at_pagamento_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emprestimo",
            name="taxa_de_juros",
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]