
# Arthur Antunes (c) Makefile for Loan Api
# Version: 0.1
# Language: Python
# Descrição dos comandos no README.md

.PHONY: build_api

build_database:
	cd database; sudo docker-compose up -d

run_database:
	cd database; sudo docker-compose up

build_api:
	poetry install; poetry shell;
