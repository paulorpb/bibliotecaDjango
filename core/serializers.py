from rest_framework import serializers
from .models import Autor, Livro, Aluno, Emprestimo

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    autor_nome = serializers.CharField(write_only=True)
    autor_detalhes = AutorSerializer(source='autor', read_only=True)
    status = serializers.ReadOnlyField()
    capa_do_livro = serializers.ImageField(required=False)

    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor_nome', 'autor_detalhes', 'estoque', 
                  'descricao', 'capa_do_livro', 'data_publicacao', 'paginas', 
                  'genero', 'status']

    def create(self, validated_data):
        autor_nome = validated_data.pop('autor_nome')
        autor_obj, _ = Autor.objects.get_or_create(nome=autor_nome)
        return Livro.objects.create(autor=autor_obj, **validated_data)

    def update(self, instance, validated_data):
        if 'autor_nome' in validated_data:
            autor_nome = validated_data.pop('autor_nome')
            autor_obj, _ = Autor.objects.get_or_create(nome=autor_nome)
            instance.autor = autor_obj
        return super().update(instance, validated_data)

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class EmprestimoSerializer(serializers.ModelSerializer):
    aluno_cpf = serializers.CharField(write_only=True, required=False)
    aluno_nome = serializers.CharField(write_only=True, required=False)
    
    # Campos de leitura para exibir na tabela
    aluno_detalhes = AlunoSerializer(source='aluno', read_only=True)
    livro_titulo = serializers.ReadOnlyField(source='livro.titulo')
    livro_capa = serializers.ImageField(source='livro.capa_do_livro', read_only=True)

    class Meta:
        model = Emprestimo
        fields = ['id', 'livro', 'livro_titulo', 'livro_capa', 'data_emprestimo', 
                  'data_devolucao', 'aluno_detalhes', 'aluno_cpf', 'aluno_nome']

    def validate(self, data):
        # Validação: Pelo menos um dos dois deve vir
        if not data.get('aluno_cpf') and not data.get('aluno_nome'):
            raise serializers.ValidationError("Informe o CPF ou o Nome do aluno.")
        return data

    def create(self, validated_data):
        cpf = validated_data.pop('aluno_cpf', None)
        nome = validated_data.pop('aluno_nome', None)
        livro = validated_data.get('livro')

        # 1. Buscar Aluno (Lógica de Prioridade: CPF > Nome)
        aluno = None
        if cpf:
            aluno = Aluno.objects.filter(cpf=cpf).first()
        elif nome:
            aluno = Aluno.objects.filter(nome__iexact=nome).first()

        if not aluno:
            raise serializers.ValidationError("Aluno não encontrado no sistema.")

        # 2. Validar Estoque
        if livro.estoque <= 0:
            raise serializers.ValidationError("Livro indisponível.")

        # 3. Executar Empréstimo
        livro.estoque -= 1
        livro.save()
        
        return Emprestimo.objects.create(aluno=aluno, **validated_data)