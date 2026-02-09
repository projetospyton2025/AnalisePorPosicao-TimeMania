"""
Aplicação Flask principal para o Sistema de Análise da Timemania.
"""
from flask import Flask
from dotenv import load_dotenv
import config
from routes import main_bp, api_bp

# Carregar variáveis de ambiente
load_dotenv()

# Criar aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['JSON_SORT_KEYS'] = False

# Registrar blueprints
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)

# Rota de teste/health check
@app.route('/health')
def health_check():
    """Verifica o status da aplicação."""
    return {
        'status': 'online',
        'version': '1.0.0',
        'name': 'Sistema de Análise da Timemania'
    }

if __name__ == '__main__':
    print(f"""
╔════════════════════════════════════════════════════════╗
║   SISTEMA DE ANÁLISE POR POSIÇÃO - TIMEMANIA          ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║   Servidor rodando em:                                 ║
║   http://{config.HOST}:{config.PORT}                                  ║
║                                                        ║
║   Endpoints disponíveis:                               ║
║   - GET  /                  -> Página principal        ║
║   - GET  /palpites          -> Gerar palpites          ║
║   - POST /api/atualizar     -> Atualizar base          ║
║   - GET  /api/estatisticas  -> Estatísticas            ║
║   - POST /api/gerar-palpite -> Gerar palpite           ║
║   - POST /api/conferir      -> Conferir palpite        ║
║                                                        ║
║   Cores da Timemania:                                  ║
║   - Amarelo: #FFF600 (números)                         ║
║   - Verde:   #12923D (time do coração)                 ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
