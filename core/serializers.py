from rest_framework import serializers
from .models import Autor, Livro, Pedido

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    # Nested serializer para mostrar o nome do autor na leitura, ou apenas ID na escrita
    nome_autor = serializers.ReadOnlyField(source='autor.nome')

    class Meta:
        model = Livro
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'