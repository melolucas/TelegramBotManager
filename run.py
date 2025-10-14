#!/usr/bin/env python3
"""
Script para executar a API do Telegram Bot Manager
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from app import app

if __name__ == '__main__':
    # Verificar se as dependências estão instaladas
    try:
        import flask
        import telegram
        import flask_cors
    except ImportError as e:
        print(f"❌ Erro: Dependência não encontrada: {e}")
        print("Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    # Configurações
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    
    print("🚀 Iniciando Telegram Bot Manager API...")
    print(f"📍 URL: http://{host}:{port}")
    print(f"🔧 Debug: {debug}")
    print("📚 Documentação: Veja docs/README.md")
    print("🧪 Teste: Execute python tests/test_api.py")
    print("\n" + "="*50)
    
    # Executar aplicação
    app.run(host=host, port=port, debug=debug)
