# Telegram Bot Manager API

Sistema para gerenciar grupos do Telegram de forma dinâmica, permitindo múltiplos usuários com diferentes bots.

## 🚀 Início Rápido

### 1. Instalação
```bash
pip install -r requirements.txt
```

### 2. Execução
```bash
# Opção 1: Arquivo principal
python main.py

# Opção 2: Script de execução
python run.py
```

### 3. Teste
```bash
python tests/test_api.py
```

## 📁 Estrutura do Projeto

```
TelegramBotManager/
├── src/                          # Código fonte
│   ├── __init__.py              # Pacote principal
│   ├── app.py                   # API Flask
│   └── telegram_bot_manager.py  # Lógica de negócio
├── tests/                        # Testes
│   ├── __init__.py
│   └── test_api.py              # Script de teste
├── docs/                         # Documentação
│   └── README.md                # Documentação completa
├── main.py                       # Ponto de entrada principal
├── run.py                        # Script de execução
├── config.py                     # Configurações
├── requirements.txt              # Dependências
├── env.example                   # Exemplo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
└── LICENSE                       # Licença
```

## 📚 Documentação

Para documentação completa da API, veja [docs/API.md](docs/API.md)

## 🔧 Configuração

1. Copie o arquivo de exemplo:
```bash
cp env.example .env
```

2. Configure as variáveis de ambiente no arquivo `.env`

## 🧪 Testando

Execute o script de teste:
```bash
python tests/test_api.py
```

## 📋 Funcionalidades

- ✅ Registrar bots para múltiplos usuários
- ✅ Gerenciar grupos do Telegram
- ✅ Adicionar/remover membros
- ✅ Enviar mensagens
- ✅ Editar configurações de grupos
- ✅ API REST completa

## 🛠️ Desenvolvimento

Para desenvolvimento, execute:
```bash
python main.py
```

A API estará disponível em `http://localhost:5000`