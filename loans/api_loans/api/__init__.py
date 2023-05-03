from rest_framework import serializers
from api.models import Emprestimo

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'