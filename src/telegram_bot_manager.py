import asyncio
import logging
from typing import Dict, List, Any
from telegram import Bot, ChatPermissions
from telegram.error import TelegramError

logger = logging.getLogger(__name__)

class TelegramBotManager:
    def __init__(self):
        self.bots: Dict[str, Bot] = {}
        self.user_bots: Dict[str, str] = {}  # user_id -> bot_token mapping
        self.groups: Dict[str, List[Dict]] = {}  # user_id -> list of groups
        
    def register_bot(self, user_id: str, bot_token: str) -> Dict[str, Any]:
        """Registrar um novo bot para um usuário"""
        try:
            # Criar instância do bot
            bot = Bot(token=bot_token)
            
            # Testar se o token é válido
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                bot_info = loop.run_until_complete(bot.get_me())
                loop.close()
            except Exception as e:
                return {"error": f"Token inválido: {str(e)}"}
            
            # Registrar o bot
            self.bots[user_id] = bot
            self.user_bots[user_id] = bot_token
            self.groups[user_id] = []
            
            return {
                "success": True,
                "message": "Bot registrado com sucesso",
                "bot_info": {
                    "id": bot_info.id,
                    "username": bot_info.username,
                    "first_name": bot_info.first_name
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao registrar bot: {str(e)}")
            return {"error": f"Erro ao registrar bot: {str(e)}"}
    
    def create_group(self, user_id: str, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar um novo grupo"""
        try:
            if user_id not in self.bots:
                return {"error": "Bot não registrado para este usuário"}
            
            bot = self.bots[user_id]
            
            # Extrair dados do grupo
            chat_id = group_data.get('chat_id')  # Para grupos existentes
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                if chat_id:
                    # Se chat_id foi fornecido, obter informações do grupo existente
                    chat = loop.run_until_complete(bot.get_chat(chat_id))
                    group_info = {
                        "id": chat.id,
                        "title": chat.title,
                        "type": chat.type,
                        "description": chat.description,
                        "invite_link": chat.invite_link,
                        "member_count": chat.member_count if hasattr(chat, 'member_count') else 0
                    }
                else:
                    # Criar novo grupo (supergrupo)
                    # Nota: A API do Telegram não permite criar grupos via bot diretamente
                    # O grupo deve ser criado manualmente e o bot adicionado
                    return {
                        "error": "Para criar um grupo, crie-o manualmente no Telegram e forneça o chat_id",
                        "instructions": "1. Crie um grupo no Telegram\n2. Adicione o bot como administrador\n3. Use o chat_id do grupo na requisição"
                    }
                
                # Adicionar grupo à lista do usuário
                if user_id not in self.groups:
                    self.groups[user_id] = []
                
                self.groups[user_id].append(group_info)
                
                return {
                    "success": True,
                    "message": "Grupo configurado com sucesso",
                    "group": group_info
                }
                
            finally:
                loop.close()
                
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao criar grupo: {str(e)}")
            return {"error": f"Erro do Telegram: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro ao criar grupo: {str(e)}")
            return {"error": f"Erro ao criar grupo: {str(e)}"}
    
    def edit_group(self, user_id: str, group_id: str, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Editar um grupo existente"""
        try:
            if user_id not in self.bots:
                return {"error": "Bot não registrado para este usuário"}
            
            bot = self.bots[user_id]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Atualizar título se fornecido
                if 'title' in group_data:
                    loop.run_until_complete(bot.set_chat_title(group_id, group_data['title']))
                
                # Atualizar descrição se fornecida
                if 'description' in group_data:
                    loop.run_until_complete(bot.set_chat_description(group_id, group_data['description']))
                
                # Atualizar permissões se fornecidas
                if 'permissions' in group_data:
                    permissions = ChatPermissions(
                        can_send_messages=group_data['permissions'].get('can_send_messages', True),
                        can_send_media_messages=group_data['permissions'].get('can_send_media_messages', True),
                        can_send_polls=group_data['permissions'].get('can_send_polls', True),
                        can_send_other_messages=group_data['permissions'].get('can_send_other_messages', True),
                        can_add_web_page_previews=group_data['permissions'].get('can_add_web_page_previews', True),
                        can_change_info=group_data['permissions'].get('can_change_info', False),
                        can_invite_users=group_data['permissions'].get('can_invite_users', False),
                        can_pin_messages=group_data['permissions'].get('can_pin_messages', False)
                    )
                    loop.run_until_complete(bot.set_chat_permissions(group_id, permissions))
                
                # Obter informações atualizadas do grupo
                chat = loop.run_until_complete(bot.get_chat(group_id))
                group_info = {
                    "id": chat.id,
                    "title": chat.title,
                    "type": chat.type,
                    "description": chat.description,
                    "invite_link": chat.invite_link,
                    "member_count": chat.member_count if hasattr(chat, 'member_count') else 0
                }
                
                # Atualizar na lista de grupos do usuário
                if user_id in self.groups:
                    for i, group in enumerate(self.groups[user_id]):
                        if str(group['id']) == str(group_id):
                            self.groups[user_id][i] = group_info
                            break
                
                return {
                    "success": True,
                    "message": "Grupo editado com sucesso",
                    "group": group_info
                }
                
            finally:
                loop.close()
                
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao editar grupo: {str(e)}")
            return {"error": f"Erro do Telegram: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro ao editar grupo: {str(e)}")
            return {"error": f"Erro ao editar grupo: {str(e)}"}
    
    def delete_group(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """Excluir um grupo (sair do grupo)"""
        try:
            if user_id not in self.bots:
                return {"error": "Bot não registrado para este usuário"}
            
            bot = self.bots[user_id]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Sair do grupo
                loop.run_until_complete(bot.leave_chat(group_id))
                
                # Remover da lista de grupos do usuário
                if user_id in self.groups:
                    self.groups[user_id] = [
                        group for group in self.groups[user_id] 
                        if str(group['id']) != str(group_id)
                    ]
                
                return {
                    "success": True,
                    "message": "Bot removido do grupo com sucesso"
                }
                
            finally:
                loop.close()
                
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao excluir grupo: {str(e)}")
            return {"error": f"Erro do Telegram: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro ao excluir grupo: {str(e)}")
            return {"error": f"Erro ao excluir grupo: {str(e)}"}
    
    def add_members(self, user_id: str, group_id: str, members: List[str]) -> Dict[str, Any]:
        """Adicionar membros ao grupo"""
        try:
            if user_id not in self.bots:
                return {"error": "Bot não registrado para este usuário"}
            
            bot = self.bots[user_id]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                added_members = []
                failed_members = []
                
                for member in members:
                    try:
                        # Adicionar membro ao grupo
                        loop.run_until_complete(bot.add_chat_member(group_id, member))
                        added_members.append(member)
                    except Exception as e:
                        failed_members.append({"user": member, "error": str(e)})
                
                return {
                    "success": True,
                    "message": f"Adicionados {len(added_members)} membros",
                    "added_members": added_members,
                    "failed_members": failed_members
                }
                
            finally:
                loop.close()
                
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao adicionar membros: {str(e)}")
            return {"error": f"Erro do Telegram: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro ao adicionar membros: {str(e)}")
            return {"error": f"Erro ao adicionar membros: {str(e)}"}
    
    def remove_members(self, user_id: str, group_id: str, members: List[str]) -> Dict[str, Any]:
        """Remover membros do grupo"""
        try:
            if user_id not in self.bots:
                return {"error": "Bot não registrado para este usuário"}
            
            bot = self.bots[user_id]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                removed_members = []
                failed_members = []
                
                for member in members:
                    try:
                        # Remover membro do grupo
                        loop.run_until_complete(bot.ban_chat_member(group_id, member))
                        # Desbanir imediatamente para permitir reentrada
                        loop.run_until_complete(bot.unban_chat_member(group_id, member))
                        removed_members.append(member)
                    except Exception as e:
                        failed_members.append({"user": member, "error": str(e)})
                
                return {
                    "success": True,
                    "message": f"Removidos {len(removed_members)} membros",
                    "removed_members": removed_members,
                    "failed_members": failed_members
                }
                
            finally:
                loop.close()
                
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao remover membros: {str(e)}")
            return {"error": f"Erro do Telegram: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro ao remover membros: {str(e)}")
            return {"error": f"Erro ao remover membros: {str(e)}"}
    
    def send_message(self, user_id: str, group_id: str, message: str, parse_mode: str = 'HTML') -> Dict[str, Any]:
        """Enviar mensagem para o grupo"""
        try:
            if user_id not in self.bots:
                return {"error": "Bot não registrado para este usuário"}
            
            bot = self.bots[user_id]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Enviar mensagem
                sent_message = loop.run_until_complete(
                    bot.send_message(
                        chat_id=group_id,
                        text=message,
                        parse_mode=parse_mode
                    )
                )
                
                return {
                    "success": True,
                    "message": "Mensagem enviada com sucesso",
                    "message_id": sent_message.message_id,
                    "date": sent_message.date.isoformat()
                }
                
            finally:
                loop.close()
                
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao enviar mensagem: {str(e)}")
            return {"error": f"Erro do Telegram: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {str(e)}")
            return {"error": f"Erro ao enviar mensagem: {str(e)}"}
    
    def list_groups(self, user_id: str) -> Dict[str, Any]:
        """Listar grupos do usuário"""
        try:
            if user_id not in self.groups:
                return {"groups": []}
            
            return {
                "success": True,
                "groups": self.groups[user_id]
            }
            
        except Exception as e:
            logger.error(f"Erro ao listar grupos: {str(e)}")
            return {"error": f"Erro ao listar grupos: {str(e)}"}
    
    def get_group_info(self, user_id: str, group_id: str) -> Dict[str, Any]:
        """Obter informações de um grupo específico"""
        try:
            if user_id not in self.bots:
                return {"error": "Bot não registrado para este usuário"}
            
            bot = self.bots[user_id]
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Obter informações do grupo
                chat = loop.run_until_complete(bot.get_chat(group_id))
                
                # Obter administradores do grupo
                administrators = loop.run_until_complete(bot.get_chat_administrators(group_id))
                admin_list = []
                for admin in administrators:
                    admin_list.append({
                        "user_id": admin.user.id,
                        "username": admin.user.username,
                        "first_name": admin.user.first_name,
                        "status": admin.status
                    })
                
                group_info = {
                    "id": chat.id,
                    "title": chat.title,
                    "type": chat.type,
                    "description": chat.description,
                    "invite_link": chat.invite_link,
                    "member_count": chat.member_count if hasattr(chat, 'member_count') else 0,
                    "administrators": admin_list
                }
                
                return {
                    "success": True,
                    "group": group_info
                }
                
            finally:
                loop.close()
                
        except TelegramError as e:
            logger.error(f"Erro do Telegram ao obter informações do grupo: {str(e)}")
            return {"error": f"Erro do Telegram: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro ao obter informações do grupo: {str(e)}")
            return {"error": f"Erro ao obter informações do grupo: {str(e)}"}
