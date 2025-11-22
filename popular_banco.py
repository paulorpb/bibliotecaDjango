import os
import django
import random
from datetime import date, timedelta

# Configuração do ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_config.settings')
django.setup()

from core.models import Livro, Autor, Aluno

# --- CONFIGURAÇÕES E LISTAS DE DADOS ---

CURSOS = [
    "Engenharia de Software", "Direito", "Medicina", "Arquitetura", 
    "Psicologia", "Administração", "Ciência da Computação", 
    "Pedagogia", "Enfermagem", "Economia", "Design Gráfico", 
    "Educação Física", "Engenharia Civil", "Biologia"
]

TURMAS = ["2022.1", "2022.2", "2023.1", "2023.2", "2024.1", "Manhã-A", "Noite-B", "Tarde-C"]

NOMES_PRIMEIROS = [
    "Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", 
    "Helena", "Igor", "Julia", "Lucas", "Mariana", "Nicolas", "Olivia", 
    "Pedro", "Rafaela", "Samuel", "Tatiane", "Vinicius", "Yasmin", 
    "João", "Maria", "José", "Leticia", "Paulo", "Amanda", "Diego"
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", 
    "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", 
    "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira"
]

# --- FUNÇÕES AUXILIARES ---

def gerar_data_aleatoria(anos_atras_inicio=2, anos_atras_fim=0):
    """Gera data para publicação de livros (recente)"""
    start_date = date.today() - timedelta(days=365 * anos_atras_inicio)
    end_date = date.today() - timedelta(days=365 * anos_atras_fim)
    time_between = end_date - start_date
    random_days = random.randrange(time_between.days + 1) if time_between.days > 0 else 0
    return start_date + timedelta(days=random_days)

def gerar_nascimento_aluno():
    """Gera data de nascimento para alunos (entre 18 e 30 anos)"""
    # Entre 18 e 30 anos atrás
    start_date = date.today() - timedelta(days=365 * 30)
    end_date = date.today() - timedelta(days=365 * 18)
    time_between = end_date - start_date
    random_days = random.randrange(time_between.days)
    return start_date + timedelta(days=random_days)

def gerar_cpf():
    """Gera um CPF formatado aleatório"""
    p1 = random.randint(1, 999)
    p2 = random.randint(1, 999)
    p3 = random.randint(1, 999)
    d = random.randint(1, 99)
    return f"{p1:03d}.{p2:03d}.{p3:03d}-{d:02d}"

def gerar_nome_completo():
    return f"{random.choice(NOMES_PRIMEIROS)} {random.choice(SOBRENOMES)}"

# --- DADOS DOS LIVROS (MANTIDO) ---
DADOS_LIVROS = [
    ("Dom Casmurro", "Machado de Assis", "Romance,Clássico"),
    ("Memórias Póstumas de Brás Cubas", "Machado de Assis", "Romance,Clássico"),
    ("O Cortiço", "Aluísio Azevedo", "Romance,Naturalismo"),
    ("Grande Sertão: Veredas", "João Guimarães Rosa", "Romance,Literatura Brasileira"),
    ("Vidas Secas", "Graciliano Ramos", "Romance,Drama"),
    ("Capitães da Areia", "Jorge Amado", "Romance,Aventura"),
    ("A Hora da Estrela", "Clarice Lispector", "Romance,Filosófico"),
    ("O Tempo e o Vento", "Erico Verissimo", "Romance,História"),
    ("Triste Fim de Policarpo Quaresma", "Lima Barreto", "Sátira,Clássico"),
    ("O Guarani", "José de Alencar", "Romance,Indigenista"),
    ("O Senhor dos Anéis: A Sociedade do Anel", "J.R.R. Tolkien", "Fantasia,Aventura"),
    ("O Hobbit", "J.R.R. Tolkien", "Fantasia,Aventura"),
    ("Harry Potter e a Pedra Filosofal", "J.K. Rowling", "Fantasia,Jovem Adulto"),
    ("Harry Potter e o Prisioneiro de Azkaban", "J.K. Rowling", "Fantasia,Mistério"),
    ("Duna", "Frank Herbert", "Sci-Fi,Aventura"),
    ("Neuromancer", "William Gibson", "Sci-Fi,Cyberpunk"),
    ("Fundação", "Isaac Asimov", "Sci-Fi,Clássico"),
    ("O Guia do Mochileiro das Galáxias", "Douglas Adams", "Sci-Fi,Humor"),
    ("1984", "George Orwell", "Distopia,Sci-Fi"),
    ("Admirável Mundo Novo", "Aldous Huxley", "Distopia,Sci-Fi"),
    ("Fahrenheit 451", "Ray Bradbury", "Distopia,Sci-Fi"),
    ("O Nome do Vento", "Patrick Rothfuss", "Fantasia,Aventura"),
    ("A Guerra dos Tronos", "George R.R. Martin", "Fantasia,Política"),
    ("Deuses Americanos", "Neil Gaiman", "Fantasia,Mistério"),
    ("Eu, Robô", "Isaac Asimov", "Sci-Fi,Contos"),
    ("Código Limpo", "Robert C. Martin", "Técnico,Programação"),
    ("O Programador Pragmático", "Andrew Hunt", "Técnico,Carreira"),
    ("Padrões de Projeto", "Erich Gamma", "Técnico,Engenharia"),
    ("Arquitetura Limpa", "Robert C. Martin", "Técnico,Arquitetura"),
    ("Refatoração", "Martin Fowler", "Técnico,Programação"),
    ("Entendendo Algoritmos", "Aditya Bhargava", "Técnico,Educação"),
    ("Python Fluente", "Luciano Ramalho", "Técnico,Python"),
    ("Use a Cabeça! Padrões de Projetos", "Eric Freeman", "Técnico,Educação"),
    ("O Design do Dia a Dia", "Don Norman", "Design,Negócios"),
    ("A Startup Enxuta", "Eric Ries", "Negócios,Empreendedorismo"),
    ("De Zero a Um", "Peter Thiel", "Negócios,Empreendedorismo"),
    ("Rápido e Devagar", "Daniel Kahneman", "Psicologia,Negócios"),
    ("Sapiens: Uma Breve História da Humanidade", "Yuval Noah Harari", "História,Antropologia"),
    ("Homo Deus", "Yuval Noah Harari", "Futurismo,Filosofia"),
    ("Steve Jobs", "Walter Isaacson", "Biografia,Tecnologia"),
    ("O Iluminado", "Stephen King", "Terror,Suspense"),
    ("It: A Coisa", "Stephen King", "Terror,Fantasia"),
    ("O Exorcista", "William Peter Blatty", "Terror,Sobrenatural"),
    ("Drácula", "Bram Stoker", "Terror,Clássico"),
    ("Frankenstein", "Mary Shelley", "Terror,Sci-Fi"),
    ("O Silêncio dos Inocentes", "Thomas Harris", "Suspense,Policial"),
    ("Garota Exemplar", "Gillian Flynn", "Suspense,Drama"),
    ("O Código Da Vinci", "Dan Brown", "Suspense,Mistério"),
    ("Anjos e Demônios", "Dan Brown", "Suspense,Mistério"),
    ("Bird Box", "Josh Malerman", "Terror,Distopia"),
    ("Orgulho e Preconceito", "Jane Austen", "Romance,Clássico"),
    ("Razão e Sensibilidade", "Jane Austen", "Romance,Clássico"),
    ("O Morro dos Ventos Uivantes", "Emily Brontë", "Romance,Gótico"),
    ("Jane Eyre", "Charlotte Brontë", "Romance,Drama"),
    ("A Culpa é das Estrelas", "John Green", "Romance,Jovem Adulto"),
    ("Como Eu Era Antes de Você", "Jojo Moyes", "Romance,Drama"),
    ("O Grande Gatsby", "F. Scott Fitzgerald", "Drama,Clássico"),
    ("Cem Anos de Solidão", "Gabriel García Márquez", "Realismo Mágico,Clássico"),
    ("O Amor nos Tempos do Cólera", "Gabriel García Márquez", "Romance,Drama"),
    ("A Menina que Roubava Livros", "Markus Zusak", "Drama,História"),
    ("O Caçador de Pipas", "Khaled Hosseini", "Drama,História"),
    ("A Cidade do Sol", "Khaled Hosseini", "Drama,História"),
    ("Os Miseráveis", "Victor Hugo", "Drama,História"),
    ("Anna Karenina", "Liev Tolstói", "Romance,Clássico"),
    ("Crime e Castigo", "Fiódor Dostoiévski", "Romance,Psicológico"),
    ("O Poder do Hábito", "Charles Duhigg", "Autoajuda,Psicologia"),
    ("Como Fazer Amigos e Influenciar Pessoas", "Dale Carnegie", "Autoajuda,Negócios"),
    ("O Milagre da Manhã", "Hal Elrod", "Autoajuda,Produtividade"),
    ("Mindset", "Carol S. Dweck", "Psicologia,Educação"),
    ("Essencialismo", "Greg McKeown", "Produtividade,Negócios"),
    ("Pai Rico, Pai Pobre", "Robert Kiyosaki", "Finanças,Autoajuda"),
    ("Os Segredos da Mente Milionária", "T. Harv Eker", "Finanças,Autoajuda"),
    ("O Homem Mais Rico da Babilônia", "George S. Clason", "Finanças,História"),
    ("A Arte da Guerra", "Sun Tzu", "Estratégia,Filosofia"),
    ("Meditações", "Marco Aurélio", "Filosofia,Estoicismo"),
    ("Torto Arado", "Itamar Vieira Junior", "Drama,Literatura Brasileira"),
    ("O Avesso da Pele", "Jeferson Tenório", "Drama,Social"),
    ("Tudo é Rio", "Carla Madeira", "Romance,Drama"),
    ("A Biblioteca da Meia-Noite", "Matt Haig", "Fantasia,Drama"),
    ("Os Sete Maridos de Evelyn Hugo", "Taylor Jenkins Reid", "Romance,Drama"),
    ("Verity", "Colleen Hoover", "Suspense,Romance"),
    ("É Assim que Acaba", "Colleen Hoover", "Romance,Drama"),
    ("Daisy Jones & The Six", "Taylor Jenkins Reid", "Música,Drama"),
    ("Mulheres Que Correm Com os Lobos", "Clarissa Pinkola Estés", "Psicologia,Feminismo"),
    ("Pequeno Manual Antirracista", "Djamila Ribeiro", "Sociedade,Filosofia"),
    ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "Infantil,Filosofia"),
    ("Alice no País das Maravilhas", "Lewis Carroll", "Fantasia,Clássico"),
    ("As Crônicas de Nárnia", "C.S. Lewis", "Fantasia,Aventura"),
    ("Percy Jackson e o Ladrão de Raios", "Rick Riordan", "Fantasia,Aventura"),
    ("Jogos Vorazes", "Suzanne Collins", "Distopia,Aventura"),
    ("Maus", "Art Spiegelman", "HQ,História"),
    ("Persépolis", "Marjane Satrapi", "HQ,Biografia"),
    ("Watchmen", "Alan Moore", "HQ,Super-heróis"),
    ("Batman: O Cavaleiro das Trevas", "Frank Miller", "HQ,Ação"),
    ("V de Vingança", "Alan Moore", "HQ,Distopia"),
    ("Sandman: Prelúdio", "Neil Gaiman", "HQ,Fantasia"),
    ("Diário de um Banana", "Jeff Kinney", "Infantil,Humor"),
    ("Extraordinário", "R.J. Palacio", "Drama,Infantil"),
    ("Malala: A Menina que Queria Ir para a Escola", "Adriana Carranca", "Biografia,Jornalismo"),
    ("Anne de Green Gables", "L.M. Montgomery", "Romance,Infantil")
]

# --- EXECUÇÃO ---

def povoar_banco():
    print("=" * 50)
    print("INICIANDO POVOAMENTO DO BANCO DE DADOS")
    print("=" * 50)

    # 1. CRIAR LIVROS E AUTORES
    contador_livros = 0
    contador_autores = 0

    print("\n>>> Gerando Livros...")
    for titulo, nome_autor, genero in DADOS_LIVROS:
        autor_obj, created_a = Autor.objects.get_or_create(nome=nome_autor)
        if created_a: contador_autores += 1

        # get_or_create evita duplicidade se rodar o script 2x
        livro_obj, created_l = Livro.objects.get_or_create(
            titulo=titulo,
            defaults={
                'autor': autor_obj,
                'genero': genero,
                'estoque': random.randint(0, 25), # Alguns podem vir zerados (Alugado)
                'paginas': random.randint(100, 900),
                'data_publicacao': gerar_data_aleatoria(),
                'descricao': f"Sinopse oficial de '{titulo}'. Uma obra que define o gênero {genero.split(',')[0]} com maestria.",
                'capa_do_livro': None
            }
        )
        if created_l: contador_livros += 1

    print(f"  -> Livros Processados. Novos Criados: {contador_livros}")

    # 2. CRIAR ALUNOS
    print("\n>>> Gerando Alunos...")
    contador_alunos = 0
    
    for _ in range(100):
        cpf_gerado = gerar_cpf()
        nome_gerado = gerar_nome_completo()
        
        aluno_obj, created_al = Aluno.objects.get_or_create(
            cpf=cpf_gerado,
            defaults={
                'nome': nome_gerado,
                'data_nascimento': gerar_nascimento_aluno(),
                'curso': random.choice(CURSOS),
                'turma': random.choice(TURMAS)
            }
        )
        if created_al: contador_alunos += 1

    print(f"  -> Alunos Processados. Novos Criados: {contador_alunos}")

    print("=" * 50)
    print("POVOAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 50)

if __name__ == '__main__':
    povoar_banco()