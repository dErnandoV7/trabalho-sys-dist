import sys
import os

# Servico de historico controla registros de audicoes por usuario

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from messaging import MessagingSystem

# Estrutura em memoria que representa o historico unificado de audicoes
HISTORICO = []

def logica_do_historico(mensagem):
    # Decide entre obter, adicionar ou limpar registros conforme a acao
    acao = mensagem.get('acao')
    
    if acao == 'obter':
        print("Obtendo histórico único")
        return {"status": "sucesso", "historico": HISTORICO}
    
    elif acao == 'adicionar':
        musica = mensagem.get('musica', {})
        HISTORICO.insert(0, musica)
        print("Música adicionada ao histórico")
        return {"status": "sucesso", "msg": "Música adicionada ao histórico"}
    
    elif acao == 'limpar':
        HISTORICO.clear()
        print("Histórico limpo")
        return {"status": "sucesso", "msg": "Histórico limpo"}
    
    return {"status": "erro", "msg": "Acao desconhecida"}

if __name__ == "__main__":
    # Abre consumo continuo da fila dedicada ao historico
    msg_system = MessagingSystem()
    msg_system.listen_and_reply('fila_historico', logica_do_historico)
