# 📋 QUICK START - SPOTIFY DISTRIBUÍDO

## ⚡ 30 SEGUNDOS - O QUE É ISSO?

Sistema de música distribuído com:
- ✅ Gateway roteador
- ✅ 3 microsserviços
- ✅ Cliente interativo
- ✅ RabbitMQ para comunicação
- ✅ RPC para sincronização

## 🚀 INICIAR EM 3 LINHAS

```bash
pip install pika
rabbitmq-server
python iniciar_sistema.py
```

Pronto! Gateway está funcionando.

## 📱 MENU DO CLIENTE

```
1. Buscar música      → Digite "queen"
2. Ver histórico      → Lista suas músicas
3. Listar playlists   → Suas playlists
4. Criar playlist     → Nome da playlist
5. Limpar histórico   → Limpa tudo
0. Sair               → Sai
```

## 🔄 COMO FUNCIONA

```
Cliente
  ↓ (envio)
Gateway (roteador)
  ↓ (direcionamento)
Serviço (processamento)
  ↓ (resposta)
Cliente
  ↓ (exibição)
Resultado!
```

## 📁 ARQUIVOS PRINCIPAIS

```
gateway.py           → Roteador central
services/catalogo.py → Busca de músicas
client_completo.py   → Interface do usuário
messaging.py         → Sistema de mensagens
```

## 🧪 TESTE RÁPIDO

1. Iniciar sistema (veja acima)
2. Aguardar "Aguardando requisições" em todos os terminais
3. Buscar "queen" no cliente
4. Ver resultado: "Bohemian Rhapsody" ✅

## 📚 DOCUMENTAÇÃO

| Documento | Tempo | Função |
|-----------|-------|--------|
| RESUMO.md | 5 min | Visão geral |
| CHECKLIST.md | 10 min | Começar |
| GATEWAY_README.md | 20 min | Guia completo |
| GUIA_RPC.md | 30 min | Técnico |

## 💡 CONCEITOS

- **Gateway**: Centraliza requisições
- **RPC**: Chamada remota síncrona
- **UUID**: Identificador único
- **Fila**: RabbitMQ para mensagens
- **Microsserviço**: Serviço independente

## 🔧 REQUISITOS

```
Python 3.x
RabbitMQ
pika (pip install pika)
```

## ⚠️ ERROS COMUNS

| Erro | Solução |
|------|---------|
| Connection refused | Inicie RabbitMQ |
| Timeout | Todos os 5 serviços iniciados? |
| Fila vazia | Reinicie gateway |

## 📍 PRÓXIMO PASSO

👉 Leia [RESUMO.md](RESUMO.md)

---

**Quick Start:** Janeiro 2026
