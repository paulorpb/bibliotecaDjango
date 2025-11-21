from django.db import models
import uuid

class Autor(models.Model):
    # O Django cria automaticamente um id (Integer, PK), mas podemos explicitar se quiser
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Autores"

class Livro(models.Model):
    titulo = models.CharField(max_length=255) # localized String simplificado
    autor = models.ForeignKey(Autor, related_name='livros', on_delete=models.CASCADE)
    estoque = models.IntegerField()
    descricao = models.TextField() # localized String simplificado
    capa_do_livro = models.URLField(max_length=500) # URL da imagem
    data_publicacao = models.DateField()
    paginas = models.IntegerField()
    genero = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo

class Pedido(models.Model):
    # UUID como chave primária
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    pais = models.CharField(max_length=100) # Representando Country
    quantidade = models.IntegerField()
    
    # Campos "managed" (controle de auditoria simples)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.livro.titulo}"