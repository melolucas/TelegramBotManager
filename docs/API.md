# Documentação da API - Telegram Bot Manager

Documentação completa da API para gerenciar grupos do Telegram.

## Funcionalidades

- ✅ **Registrar Bots**: Cadastrar bots do Telegram para diferentes usuários
- ✅ **Criar Grupos**: Configurar grupos existentes (o grupo deve ser criado manualmente no Telegram)
- ✅ **Editar Grupos**: Modificar título, descrição e permissões dos grupos
- ✅ **Excluir Grupos**: Remover o bot de grupos
- ✅ **Gerenciar Membros**: Adicionar e remover membros dos grupos
- ✅ **Enviar Mensagens**: Enviar mensagens para os grupos
- ✅ **Listar Grupos**: Obter lista de grupos do usuário
- ✅ **Informações do Grupo**: Obter detalhes completos de um grupo

## Uso da API

### O que é o USER_ID?

O `USER_ID` é um identificador único que você define para cada usuário do seu sistema. É usado para:

- **Identificar qual bot usar**: Cada usuário pode ter seu próprio bot do Telegram
- **Isolar dados**: Os grupos e operações ficam separados por usuário
- **Controle de acesso**: Permite gerenciar múltiplos usuários na mesma API

**Fluxo de trabalho:**
1. Usuário faz login no seu sistema
2. Sistema obtém o USER_ID do usuário autenticado
3. Sistema chama a API Python passando o USER_ID
4. API Python identifica qual bot usar baseado no USER_ID
5. Operações são executadas com o bot correto do usuário

**Exemplos de USER_ID:**
- `"usuario123"` - ID simples
- `"empresa_abc_funcionario_001"` - ID estruturado
- `"12345"` - ID numérico
- `"admin"` - ID administrativo

**Como escolher o USER_ID:**
- Use o mesmo ID que você usa no seu sistema principal
- Pode ser o ID do usuário, email, ou qualquer identificador único
- Deve ser consistente para o mesmo usuário
- Evite caracteres especiais e espaços

### 1. Registrar um Bot

```http
POST /bot/register
Content-Type: application/json

{
    "user_id": "usuario123",
    "bot_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
}
```

### 2. Configurar um Grupo Existente

```http
POST /bot/usuario123/group/create
Content-Type: application/json

{
    "chat_id": "-1001234567890",
    "title": "Meu Grupo",
    "description": "Descrição do grupo"
}
```

### 3. Editar um Grupo

```http
PUT /bot/usuario123/group/-1001234567890/edit
Content-Type: application/json

{
    "title": "Novo Título",
    "description": "Nova descrição",
    "permissions": {
        "can_send_messages": true,
        "can_send_media_messages": true,
        "can_send_polls": false,
        "can_send_other_messages": false,
        "can_add_web_page_previews": true,
        "can_change_info": false,
        "can_invite_users": false,
        "can_pin_messages": false
    }
}
```

### 4. Adicionar Membros

```http
POST /bot/usuario123/group/-1001234567890/members/add
Content-Type: application/json

{
    "members": ["@username1", "123456789", "@username2"]
}
```

### 5. Remover Membros

```http
POST /bot/usuario123/group/-1001234567890/members/remove
Content-Type: application/json

{
    "members": ["@username1", "123456789"]
}
```

### 6. Enviar Mensagem

```http
POST /bot/usuario123/group/-1001234567890/send-message
Content-Type: application/json

{
    "message": "Olá! Esta é uma mensagem do bot.",
    "parse_mode": "HTML"
}
```

### 7. Listar Grupos

```http
GET /bot/usuario123/groups
```

### 8. Obter Informações do Grupo

```http
GET /bot/usuario123/group/-1001234567890/info
```

### 9. Excluir Grupo (Remover Bot)

```http
DELETE /bot/usuario123/group/-1001234567890/delete
```

## Estrutura de Respostas

### Sucesso
```json
{
    "success": true,
    "message": "Operação realizada com sucesso",
    "data": { ... }
}
```

### Erro
```json
{
    "error": "Descrição do erro"
}
```

## Códigos de Status HTTP

- `200` - Sucesso
- `400` - Erro na requisição (dados inválidos)
- `500` - Erro interno do servidor

## Como Obter o Chat ID de um Grupo

1. Adicione o bot ao grupo
2. Torne o bot administrador
3. Envie uma mensagem no grupo
4. Acesse: `https://api.telegram.org/bot<SEU_BOT_TOKEN>/getUpdates`
5. Procure pelo `chat.id` do grupo (será um número negativo)

## Consumindo a API

A API pode ser consumida por qualquer linguagem que suporte HTTP. Exemplos:

### JavaScript/Fetch
```javascript
// Registrar bot
const response = await fetch('http://localhost:5000/bot/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        user_id: 'usuario123',
        bot_token: 'seu_token_aqui'
    })
});

// Enviar mensagem
const response = await fetch('http://localhost:5000/bot/usuario123/group/-1001234567890/send-message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: 'Mensagem da API!',
        parse_mode: 'HTML'
    })
});
```

### Python/Requests
```python
import requests

# Registrar bot
response = requests.post('http://localhost:5000/bot/register', json={
    'user_id': 'usuario123',
    'bot_token': 'seu_token_aqui'
})

# Enviar mensagem
response = requests.post('http://localhost:5000/bot/usuario123/group/-1001234567890/send-message', json={
    'message': 'Mensagem da API!',
    'parse_mode': 'HTML'
})
```

## Notas Importantes

1. **Criação de Grupos**: A API do Telegram não permite criar grupos via bot. O grupo deve ser criado manualmente e o bot adicionado como administrador.

2. **Permissões**: O bot precisa ter as permissões adequadas no grupo para realizar as operações.

3. **Rate Limiting**: O Telegram tem limites de taxa. A API implementa tratamento de erros para isso.

4. **Múltiplos Usuários**: Cada usuário pode ter seu próprio bot registrado.

5. **Segurança**: Mantenha os tokens dos bots seguros e não os exponha em logs ou respostas da API.

## Logs

Os logs são exibidos no console e incluem informações sobre:
- Registro de bots
- Operações nos grupos
- Erros da API do Telegram
- Requisições HTTP
