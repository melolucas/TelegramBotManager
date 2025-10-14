#!/usr/bin/env python3
"""
Script de teste para a API do Telegram Bot Manager
"""

import requests
import json
import time
import sys
from pathlib import Path

# Adicionar o diretório src ao path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Configurações
BASE_URL = "http://localhost:5000"
USER_ID = "test_user_123"
BOT_TOKEN = "SEU_BOT_TOKEN_AQUI"  # Substitua pelo token real
GROUP_ID = "-1001234567890"  # Substitua pelo ID real do grupo

def test_api():
    """Testar todas as funcionalidades da API"""
    
    print("🚀 Iniciando testes da API...")
    
    # 1. Testar health check
    print("\n1. Testando health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 2. Registrar bot
    print("\n2. Registrando bot...")
    response = requests.post(f"{BASE_URL}/bot/register", json={
        "user_id": USER_ID,
        "bot_token": BOT_TOKEN
    })
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    if response.status_code != 200:
        print("❌ Erro ao registrar bot. Verifique o token.")
        return
    
    # 3. Configurar grupo
    print("\n3. Configurando grupo...")
    response = requests.post(f"{BASE_URL}/bot/{USER_ID}/group/create", json={
        "chat_id": GROUP_ID,
        "title": "Grupo de Teste",
        "description": "Grupo criado para testes da API"
    })
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 4. Listar grupos
    print("\n4. Listando grupos...")
    response = requests.get(f"{BASE_URL}/bot/{USER_ID}/groups")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 5. Obter informações do grupo
    print("\n5. Obtendo informações do grupo...")
    response = requests.get(f"{BASE_URL}/bot/{USER_ID}/group/{GROUP_ID}/info")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 6. Editar grupo
    print("\n6. Editando grupo...")
    response = requests.put(f"{BASE_URL}/bot/{USER_ID}/group/{GROUP_ID}/edit", json={
        "title": "Grupo de Teste Atualizado",
        "description": "Descrição atualizada do grupo",
        "permissions": {
            "can_send_messages": True,
            "can_send_media_messages": True,
            "can_send_polls": False,
            "can_send_other_messages": False,
            "can_add_web_page_previews": True,
            "can_change_info": False,
            "can_invite_users": False,
            "can_pin_messages": False
        }
    })
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 7. Enviar mensagem
    print("\n7. Enviando mensagem...")
    response = requests.post(f"{BASE_URL}/bot/{USER_ID}/group/{GROUP_ID}/send-message", json={
        "message": "🤖 <b>Teste da API</b>\n\nEsta é uma mensagem de teste enviada pela API do Telegram Bot Manager!",
        "parse_mode": "HTML"
    })
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 8. Adicionar membros (exemplo - substitua pelos IDs reais)
    print("\n8. Testando adição de membros...")
    response = requests.post(f"{BASE_URL}/bot/{USER_ID}/group/{GROUP_ID}/members/add", json={
        "members": ["@username_exemplo"]  # Substitua por um username real
    })
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    # 9. Remover membros (exemplo)
    print("\n9. Testando remoção de membros...")
    response = requests.post(f"{BASE_URL}/bot/{USER_ID}/group/{GROUP_ID}/members/remove", json={
        "members": ["@username_exemplo"]  # Substitua por um username real
    })
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    print("\n✅ Testes concluídos!")

def test_with_real_data():
    """Teste com dados reais - configure antes de executar"""
    print("⚠️  ATENÇÃO: Configure BOT_TOKEN e GROUP_ID antes de executar este teste!")
    print("1. Obtenha um token de bot do @BotFather no Telegram")
    print("2. Crie um grupo e adicione o bot como administrador")
    print("3. Obtenha o chat_id do grupo")
    print("4. Atualize as variáveis BOT_TOKEN e GROUP_ID neste arquivo")
    print("5. Execute: python test_api.py")

if __name__ == "__main__":
    if BOT_TOKEN == "SEU_BOT_TOKEN_AQUI" or GROUP_ID == "-1001234567890":
        test_with_real_data()
    else:
        test_api()
