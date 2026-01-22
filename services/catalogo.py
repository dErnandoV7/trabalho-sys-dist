import sys
import os

# Servico de catalogo responde buscas por titulo ou artista via RabbitMQ

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from messaging import MessagingSystem

# Base estatica que simula uma tabela de musicas disponiveis
MUSICAS = [
    {"id": 1, "titulo": "Evidencias", "artista": "Xitaozinho", "genero": "Sertanejo"},
    {"id": 2, "titulo": "Bohemian Rhapsody", "artista": "Queen", "genero": "Rock"},
    {"id": 3, "titulo": "Smells Like Teen Spirit", "artista": "Nirvana", "genero": "Grunge"},
    {"id": 4, "titulo": "Caneta Azul", "artista": "Manoel Gomes", "genero": "Meme"},
]

def logica_do_catalogo(mensagem):
    # Interpreta a acao solicitada e busca correspondencias no catalogo local
    acao = mensagem.get('acao')
    
    if acao == 'buscar':
        termo = mensagem.get('termo', '').lower()
        print(f"Processando busca por: {termo}")
        
        resultado = [
            m for m in MUSICAS 
            if termo in m['titulo'].lower() or termo in m['artista'].lower()
        ]
        return {"status": "sucesso", "musicas": resultado}
    
    return {"status": "erro", "msg": "Acao desconhecida"}

if __name__ == "__main__":
    # Inicializa o loop de consumo na fila dedicada ao catalogo
    msg_system = MessagingSystem()
    msg_system.listen_and_reply('fila_catalogo', logica_do_catalogo)