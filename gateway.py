from messaging import MessagingSystem
import json
from datetime import datetime

# Gateway centraliza roteamento das requisoes entre filas de servicos diferentes

class GatewayAPI:
    def __init__(self):
        # Um canal recebe requisicoes externas e outro encaminha chamadas aos servicos
        self.msg_system = MessagingSystem()
        self.rpc_system = MessagingSystem()
    
    def processar_requisicao(self, mensagem):
        # Inspeciona campos da mensagem e encaminha para a fila responsavel
        servico = mensagem.get('servico')
        acao = mensagem.get('acao')
        
        print(f"[GATEWAY] Recebido: servico='{servico}', acao='{acao}'")
        
        if servico == 'catalogo':
            print(f"[GATEWAY] Roteando para fila_catalogo")
            resposta_catalogo = self.rpc_system.call_rpc('fila_catalogo', {
                'acao': acao,
                'termo': mensagem.get('termo', '')
            })
            if acao == 'buscar' and resposta_catalogo.get('status') == 'sucesso':
                for musica in resposta_catalogo.get('musicas', []):
                    musica_historico = {
                        **musica,
                        'data': datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    self.rpc_system.call_rpc('fila_historico', {
                        'acao': 'adicionar',
                        'musica': musica_historico
                    })
            return resposta_catalogo
        
        elif servico == 'playlists':
            print(f"[GATEWAY] Roteando para fila_playlists")
            return self.rpc_system.call_rpc('fila_playlists', mensagem)
        
        elif servico == 'historico':
            print(f"[GATEWAY] Roteando para fila_historico")
            return self.rpc_system.call_rpc('fila_historico', mensagem)
        
        else:
            print(f"[GATEWAY] Erro: Serviço '{servico}' desconhecido")
            return {"status": "erro", "msg": f"Serviço '{servico}' desconhecido"}
    
    def iniciar(self):
        # Mantem o loop de consumo aguardando requisicoes sincronas dos clientes
        self.msg_system.listen_and_reply('fila_gateway', self.processar_requisicao)

if __name__ == "__main__":
    print("=== GATEWAY INICIADO ===")
    gateway = GatewayAPI()
    gateway.iniciar()