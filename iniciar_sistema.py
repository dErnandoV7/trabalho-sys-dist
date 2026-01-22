import os
import sys
import time

# Script utilitario que abre cada servico do ecossistema em janelas separadas

def main():
    print("="*50)
    print("🚀 INICIANDO SISTEMA DISTRIBUÍDO")
    print("="*50)

    # Descobre o interpretador atual para reutilizar nas janelas spawnadas
    python_exec = sys.executable
    
    if " " in python_exec:
        python_exec = f'"{python_exec}"'

    # Define titulo da janela e script alvo de cada processo iniciado
    comandos = [
        ("Gateway", "gateway.py"),
        ("Catalogo", "services/catalogo.py"),
        ("Historico", "services/historico.py"),
        ("Playlists", "services/playlists.py"),
        ("CLIENTE", "client_completo.py")
    ]

    for titulo, script in comandos:
        # Usa o comando start do Windows para abrir nova janela de terminal
        print(f"Abrindo {titulo}...")
        comando_windows = f'start "{titulo}" cmd /k {python_exec} {script}'
        
        os.system(comando_windows)
        # Pequena espera evita disparar varios terminais simultaneos ao mesmo tempo
        time.sleep(1)

    print("\n✅ Tudo aberto! Verifique as novas janelas.")

if __name__ == "__main__":
    main()