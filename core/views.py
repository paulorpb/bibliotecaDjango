from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Autor, Livro, Aluno, Emprestimo
from .serializers import AutorSerializer, LivroSerializer, AlunoSerializer, EmprestimoSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all().order_by('-data_emprestimo')
    serializer_class = EmprestimoSerializer

    # Endpoint personalizado para devolver: POST /api/emprestimos/devolver/
    @action(detail=False, methods=['post'])
    def devolver(self, request):
        cpf = request.data.get('cpf')
        nome = request.data.get('nome')
        livro_id = request.data.get('livro_id')

        if not livro_id or (not cpf and not nome):
            return Response({'erro': 'Informe Livro ID e (CPF ou Nome).'}, status=status.HTTP_400_BAD_REQUEST)

        # Busca empréstimo ATIVO (data_devolucao IS NULL)
        query = Emprestimo.objects.filter(livro_id=livro_id, data_devolucao__isnull=True)
        
        if cpf:
            query = query.filter(aluno__cpf=cpf)
        elif nome:
            query = query.filter(aluno__nome__iexact=nome)

        emprestimo = query.first()

        if not emprestimo:
            return Response({'erro': 'Empréstimo ativo não encontrado para este aluno/livro.'}, status=status.HTTP_404_NOT_FOUND)

        # Processa devolução
        emprestimo.data_devolucao = timezone.now()
        emprestimo.save()

        # Devolve estoque
        livro = emprestimo.livro
        livro.estoque += 1
        livro.save()

        return Response({'mensagem': 'Livro devolvido com sucesso!'})
