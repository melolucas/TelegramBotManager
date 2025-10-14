from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from telegram_bot_manager import TelegramBotManager
import logging

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Instância global do gerenciador de bots
bot_manager = TelegramBotManager()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({"status": "healthy", "message": "Telegram Bot Manager API está funcionando"})

@app.route('/bot/register', methods=['POST'])
def register_bot():
    """Registrar um novo bot para um usuário"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        bot_token = data.get('bot_token')
        
        if not user_id or not bot_token:
            return jsonify({"error": "user_id e bot_token são obrigatórios"}), 400
        
        result = bot_manager.register_bot(user_id, bot_token)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao registrar bot: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/group/create', methods=['POST'])
def create_group(user_id):
    """Criar um novo grupo"""
    try:
        data = request.get_json()
        result = bot_manager.create_group(user_id, data)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao criar grupo: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/group/<group_id>/edit', methods=['PUT'])
def edit_group(user_id, group_id):
    """Editar um grupo existente"""
    try:
        data = request.get_json()
        result = bot_manager.edit_group(user_id, group_id, data)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao editar grupo: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/group/<group_id>/delete', methods=['DELETE'])
def delete_group(user_id, group_id):
    """Excluir um grupo"""
    try:
        result = bot_manager.delete_group(user_id, group_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao excluir grupo: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/group/<group_id>/members/add', methods=['POST'])
def add_members(user_id, group_id):
    """Adicionar membros ao grupo"""
    try:
        data = request.get_json()
        members = data.get('members', [])
        result = bot_manager.add_members(user_id, group_id, members)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao adicionar membros: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/group/<group_id>/members/remove', methods=['POST'])
def remove_members(user_id, group_id):
    """Remover membros do grupo"""
    try:
        data = request.get_json()
        members = data.get('members', [])
        result = bot_manager.remove_members(user_id, group_id, members)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao remover membros: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/group/<group_id>/send-message', methods=['POST'])
def send_message(user_id, group_id):
    """Enviar mensagem para o grupo"""
    try:
        data = request.get_json()
        message = data.get('message')
        parse_mode = data.get('parse_mode', 'HTML')
        
        if not message:
            return jsonify({"error": "Mensagem é obrigatória"}), 400
        
        result = bot_manager.send_message(user_id, group_id, message, parse_mode)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/groups', methods=['GET'])
def list_groups(user_id):
    """Listar grupos do usuário"""
    try:
        result = bot_manager.list_groups(user_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao listar grupos: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/bot/<user_id>/group/<group_id>/info', methods=['GET'])
def get_group_info(user_id, group_id):
    """Obter informações de um grupo específico"""
    try:
        result = bot_manager.get_group_info(user_id, group_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Erro ao obter informações do grupo: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
