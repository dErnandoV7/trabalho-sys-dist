import sys
import os

# Servico de playlists administra colecoes de musicas por usuario

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from messaging import MessagingSystem

# Estrutura em memoria que espelha playlists e suas musicas para um unico usuario
PLAYLISTS = [
    {
        "id": 1,
        "nome": "Meu Rock",
        "musicas": [
            {"id": 2, "titulo": "Bohemian Rhapsody", "artista": "Queen"},
            {"id": 3, "titulo": "Smells Like Teen Spirit", "artista": "Nirvana"}
        ]
    },
    {
        "id": 2,
        "nome": "Sertanejo",
        "musicas": [
            {"id": 1, "titulo": "Evidencias", "artista": "Xitaozinho"}
        ]
    },
    {
        "id": 3,
        "nome": "Favoritas",
        "musicas": [
            {"id": 4, "titulo": "Caneta Azul", "artista": "Manoel Gomes"}
        ]
    }
]

def logica_de_playlists(mensagem):
    # Implementa operacoes CRUD basicas sobre as playlists do usuario
    acao = mensagem.get('acao')
    if acao == 'listar':
        print("Listando playlists")
        return {"status": "sucesso", "playlists": PLAYLISTS}
    
    elif acao == 'criar':
        nome = mensagem.get('nome', 'Nova Playlist')
        novo_id = max((playlist['id'] for playlist in PLAYLISTS), default=0) + 1
        nova_playlist = {
            "id": novo_id,
            "nome": nome,
            "musicas": []
        }
        PLAYLISTS.append(nova_playlist)
        print(f"Playlist '{nome}' criada")
        return {"status": "sucesso", "msg": f"Playlist '{nome}' criada"}
    
    elif acao == 'adicionar_musica':
        playlist_id = mensagem.get('playlist_id')
        musica = mensagem.get('musica', {})
        for playlist in PLAYLISTS:
            if playlist['id'] == playlist_id:
                playlist['musicas'].append(musica)
                print(f"Música adicionada à playlist {playlist_id}")
                return {"status": "sucesso", "msg": "Música adicionada"}
        return {"status": "erro", "msg": "Playlist não encontrada"}
    
    elif acao == 'deletar':
        playlist_id = mensagem.get('playlist_id')
        original_len = len(PLAYLISTS)
        PLAYLISTS[:] = [p for p in PLAYLISTS if p['id'] != playlist_id]
        if len(PLAYLISTS) != original_len:
            print(f"Playlist {playlist_id} deletada")
            return {"status": "sucesso", "msg": "Playlist deletada"}
        return {"status": "erro", "msg": "Playlist não encontrada"}
    
    return {"status": "erro", "msg": "Acao desconhecida"}

if __name__ == "__main__":
    # Inicia o consumidor atrelado a fila de playlists
    msg_system = MessagingSystem()
    msg_system.listen_and_reply('fila_playlists', logica_de_playlists)
