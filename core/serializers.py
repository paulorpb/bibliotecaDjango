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
    # Campos para receber os dados do aluno no mesmo formulário
    aluno_cpf = serializers.CharField(write_only=True)
    aluno_nome = serializers.CharField(write_only=True, required=False)
    aluno_nascimento = serializers.DateField(write_only=True, required=False)
    aluno_curso = serializers.CharField(write_only=True, required=False)
    aluno_turma = serializers.CharField(write_only=True, required=False)

    # Mostrar detalhes na resposta
    aluno_detalhes = AlunoSerializer(source='aluno', read_only=True)
    livro_titulo = serializers.ReadOnlyField(source='livro.titulo')

    class Meta:
        model = Emprestimo
        fields = ['id', 'livro', 'livro_titulo', 'data_emprestimo', 
                  'aluno_detalhes', 'aluno_cpf', 'aluno_nome', 
                  'aluno_nascimento', 'aluno_curso', 'aluno_turma']

    def create(self, validated_data):
        # 1. Extrair dados do aluno
        cpf = validated_data.pop('aluno_cpf')
        nome = validated_data.pop('aluno_nome', '')
        nasc = validated_data.pop('aluno_nascimento', None)
        curso = validated_data.pop('aluno_curso', '')
        turma = validated_data.pop('aluno_turma', '')
        livro = validated_data.get('livro')

        # 2. Verificar Estoque
        if livro.estoque <= 0:
            raise serializers.ValidationError("Este livro não está disponível no momento.")

        # 3. Lógica Upsert do Aluno (Busca por CPF, se não achar, cria)
        aluno_obj, created = Aluno.objects.get_or_create(
            cpf=cpf,
            defaults={
                'nome': nome,
                'data_nascimento': nasc,
                'curso': curso,
                'turma': turma
            }
        )

        # Se o aluno já existia mas mandaram dados novos, podemos atualizar (opcional)
        if not created and nome:
            aluno_obj.nome = nome
            aluno_obj.curso = curso
            aluno_obj.turma = turma
            aluno_obj.save()

        # 4. Baixar Estoque
        livro.estoque -= 1
        livro.save()

        # 5. Criar Empréstimo
        emprestimo = Emprestimo.objects.create(aluno=aluno_obj, **validated_data)
        return emprestimo