from messaging import MessagingSystem
import os

# Cliente completo que orquestra buscas, historico e playlists via chamadas RPC ao gateway

msg_system = MessagingSystem()

def exibir_tabela(dados, colunas):
    # Monta uma tabela flexivel calculando larguras dinamicas das colunas
    if not dados:
        print("Nenhum resultado encontrado.\n")
        return
    
    larguras = {col: len(col) for col in colunas}
    for item in dados:
        for col in colunas:
            larguras[col] = max(larguras[col], len(str(item.get(col, ""))))
    
    print("-" * (sum(larguras.values()) + len(colunas) * 3 + 1))
    header = " | ".join(f"{col:<{larguras[col]}}" for col in colunas)
    print(header)
    print("-" * (sum(larguras.values()) + len(colunas) * 3 + 1))
    
    for item in dados:
        linha = " | ".join(f"{str(item.get(col, '')):<{larguras[col]}}" for col in colunas)
        print(linha)
    
    print("-" * (sum(larguras.values()) + len(colunas) * 3 + 1))
    print()

def buscar_musica():
    # Fluxo que solicita termo de busca e consulta o servico de catalogo
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== BUSCAR MÚSICA ===\n")
    
    termo = input("Digite o nome da música ou artista: ").strip()
    if not termo:
        return
    
    print("\nBuscando...")
    resposta = msg_system.call_rpc('fila_gateway', {
        "servico": "catalogo",
        "acao": "buscar",
        "termo": termo
    })
    
    if resposta['status'] == 'sucesso':
        musicas = resposta['musicas']
        if musicas:
            print(f"\nMúsicas encontradas ({len(musicas)}):")
            exibir_tabela(musicas, ['id', 'titulo', 'artista', 'genero'])
        else:
            print("\nNenhuma música encontrada.\n")
    else:
        print(f"Erro: {resposta.get('msg')}\n")
    
    input("Pressione Enter para voltar...")

def ver_historico():
    # Requisita ao servico de historico o registro acumulado
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== HISTÓRICO DE MÚSICAS ===\n")
    
    resposta = msg_system.call_rpc('fila_gateway', {
        "servico": "historico",
        "acao": "obter"
    })
    
    if resposta['status'] == 'sucesso':
        historico = resposta['historico']
        if historico:
            print(f"Histórico ({len(historico)} músicas):")
            exibir_tabela(historico, ['id', 'titulo', 'artista', 'data'])
        else:
            print("Histórico vazio.\n")
    else:
        print(f"Erro: {resposta.get('msg')}\n")
    
    input("Pressione Enter para voltar...")

def listar_playlists():
    # Lista playlists e musicas do catalogo unico
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== PLAYLISTS ===\n")
    
    resposta = msg_system.call_rpc('fila_gateway', {
        "servico": "playlists",
        "acao": "listar"
    })
    
    if resposta['status'] == 'sucesso':
        playlists = resposta['playlists']
        if playlists:
            for pl in playlists:
                print(f"\n📋 {pl['nome']} (ID: {pl['id']}) - {len(pl['musicas'])} músicas")
                if pl['musicas']:
                    exibir_tabela(pl['musicas'], ['id', 'titulo', 'artista'])
        else:
            print("Nenhuma playlist criada.\n")
    else:
        print(f"Erro: {resposta.get('msg')}\n")
    
    input("Pressione Enter para voltar...")

def criar_playlist():
    # Gera uma nova playlist vazia solicitando acao ao servico remoto
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== CRIAR PLAYLIST ===\n")
    
    nome = input("Digite o nome da playlist: ").strip()
    if not nome:
        return
    
    resposta = msg_system.call_rpc('fila_gateway', {
        "servico": "playlists",
        "acao": "criar",
        "nome": nome
    })
    
    if resposta['status'] == 'sucesso':
        print(f"\n✓ {resposta.get('msg')}\n")
    else:
        print(f"Erro: {resposta.get('msg')}\n")
    
    input("Pressione Enter para voltar...")

def limpar_historico():
    # Confirma com o usuario e limpa o historico remoto caso aprovado
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== LIMPAR HISTÓRICO ===\n")
    
    confirma = input("Tem certeza? (s/n): ").lower()
    if confirma != 's':
        return
    
    resposta = msg_system.call_rpc('fila_gateway', {
        "servico": "historico",
        "acao": "limpar"
    })
    
    if resposta['status'] == 'sucesso':
        print(f"\n✓ {resposta.get('msg')}\n")
    else:
        print(f"Erro: {resposta.get('msg')}\n")
    
    input("Pressione Enter para voltar...")

def menu_principal():
    # Loop principal que direciona para cada fluxo de acordo com a opcao digitada
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 50)
        print("🎵 SPOTIFY DISTRIBUÍDO - CLIENTE")
        print("=" * 50)
        print("1. Buscar música")
        print("2. Ver histórico")
        print("3. Listar playlists")
        print("4. Criar playlist")
        print("5. Limpar histórico")
        print("0. Sair")
        print("=" * 50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            buscar_musica()
        elif opcao == '2':
            ver_historico()
        elif opcao == '3':
            listar_playlists()
        elif opcao == '4':
            criar_playlist()
        elif opcao == '5':
            limpar_historico()
        elif opcao == '0':
            print("\nAté logo! 👋\n")
            break
        else:
            print("Opção inválida!")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nSistema interrompido.")
    except Exception as e:
        print(f"Erro: {e}")
