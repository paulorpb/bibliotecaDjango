from django.db import models
import uuid
from datetime import date

class Autor(models.Model):
    nome = models.CharField(max_length=255, unique=True) # Unique para evitar duplicatas exatas

    def __str__(self): return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(Autor, related_name='livros', on_delete=models.CASCADE)
    estoque = models.IntegerField()
    descricao = models.TextField()
    capa_do_livro = models.ImageField(upload_to='capas/', blank=True, null=True)
    data_publicacao = models.DateField()
    paginas = models.IntegerField()
    genero = models.CharField(max_length=255)

    def __str__(self): return self.titulo

    # NOVO: Propriedade dinâmica de status
    @property
    def status(self):
        return "Disponível" if self.estoque > 0 else "Emprestado"

class Aluno(models.Model):
    cpf = models.CharField(max_length=14, primary_key=True) # Ex: 000.000.000-00
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    curso = models.CharField(max_length=100)
    turma = models.CharField(max_length=50)

    def __str__(self): return f"{self.nome} ({self.cpf})"

class Emprestimo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    livro = models.ForeignKey('Livro', on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True) # Novo Campo

    def __str__(self):
        return f"{self.aluno.nome} - {self.livro.titulo}"