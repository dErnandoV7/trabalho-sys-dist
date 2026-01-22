from messaging import MessagingSystem
import os

# Cliente interativo minimalista que consulta o gateway distribuido por linha de comando

msg_system = MessagingSystem()

def exibir_tabela(dados):
    # Organiza o retorno do catalogo em formato de tabela fixa
    print("-" * 60)
    print(f"{'ID':<5} | {'ARTISTA':<20} | {'MÚSICA':<30}")
    print("-" * 60)
    
    for m in dados:
        print(f"{m['id']:<5} | {m['artista']:<20} | {m['titulo']:<30}")
    
    print("-" * 60)
    print("\n")

while True:
    # Loop principal limpa a tela, coleta termo de busca e chama o gateway
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== SPOTIFY DISTRIBUÍDO (CLIENTE) ===")
    
    busca = input("Digite o nome da música ou artista (ou 'sair'): ")

    if busca.lower() == 'sair':
        break

    print(f"\nBuscando...")
    
    # Envia uma chamada RPC para o gateway com a acao desejada
    resposta = msg_system.call_rpc('fila_gateway', {
        "servico": "catalogo",
        "acao": "buscar", 
        "termo": busca
    })

    # Trata os cenarios de sucesso e erro retornados pelo catalogo
    if resposta['status'] == 'sucesso':
        musicas = resposta['musicas']
        if musicas:
            print(f"Músicas encontradas ({len(musicas)}):")
            exibir_tabela(musicas)
        else:
            print("Nenhuma música encontrada com esse nome.")
    else:
        print(f"{resposta.get('msg')}")
    
    input("Pressione Enter para buscar novamente...")