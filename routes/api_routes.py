"""
Rotas da API REST para o sistema de análise da Timemania.
"""
from flask import Blueprint, jsonify, request
from services.api_caixa_service import ApiCaixaService
from services.estatistica_service import EstatisticaService
from services.timemania_service import TimemaniaService
from models.resultado_model import ResultadoModel

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Instanciar serviços
api_caixa_service = ApiCaixaService()
estatistica_service = EstatisticaService()
timemania_service = TimemaniaService()
resultado_model = ResultadoModel()


@api_bp.route('/atualizar', methods=['POST'])
def atualizar():
    """
    Atualiza a base de dados com os concursos mais recentes.
    
    Returns:
        JSON com resultado da atualização
    """
    try:
        resultado = api_caixa_service.atualizar_base_completa()
        return jsonify(resultado), 200 if resultado.get('sucesso') else 500
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao atualizar base: {str(e)}'
        }), 500


@api_bp.route('/ultimo-resultado', methods=['GET'])
def ultimo_resultado():
    """
    Retorna o último resultado cadastrado.
    
    Returns:
        JSON com o último resultado
    """
    try:
        resultado = resultado_model.buscar_ultimo()
        if resultado:
            return jsonify({
                'sucesso': True,
                'resultado': resultado
            }), 200
        else:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Nenhum resultado encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao buscar último resultado: {str(e)}'
        }), 500


@api_bp.route('/resultados', methods=['GET'])
def resultados():
    """
    Lista resultados com paginação.
    
    Query params:
        limite: Quantidade de resultados (padrão: todos)
    
    Returns:
        JSON com lista de resultados
    """
    try:
        limite = request.args.get('limite', type=int)
        resultados_list = resultado_model.buscar_todos(limite)
        
        return jsonify({
            'sucesso': True,
            'total': len(resultados_list),
            'resultados': resultados_list
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao buscar resultados: {str(e)}'
        }), 500


@api_bp.route('/resultado/<int:numero>', methods=['GET'])
def resultado_especifico(numero):
    """
    Busca um resultado específico pelo número do concurso.
    
    Args:
        numero: Número do concurso
    
    Returns:
        JSON com o resultado do concurso
    """
    try:
        resultado = resultado_model.buscar_por_numero(numero)
        if resultado:
            return jsonify({
                'sucesso': True,
                'resultado': resultado
            }), 200
        else:
            return jsonify({
                'sucesso': False,
                'mensagem': f'Concurso {numero} não encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao buscar resultado: {str(e)}'
        }), 500


@api_bp.route('/estatisticas', methods=['GET'])
def estatisticas():
    """
    Retorna todas as estatísticas calculadas.
    
    Returns:
        JSON com estatísticas completas
    """
    try:
        stats = estatistica_service.calcular_estatisticas_completas()
        return jsonify({
            'sucesso': True,
            'estatisticas': stats
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao calcular estatísticas: {str(e)}'
        }), 500


@api_bp.route('/estatisticas/times-coracao', methods=['GET'])
def estatisticas_times_coracao():
    """
    Retorna estatísticas específicas dos times do coração.
    
    Returns:
        JSON com estatísticas dos times
    """
    try:
        stats = {
            'frequencia': estatistica_service.calcular_frequencia_times_coracao(),
            'mais_sorteados': estatistica_service.calcular_times_mais_sorteados(10),
            'mais_atrasados': estatistica_service.calcular_times_mais_atrasados(10)
        }
        return jsonify({
            'sucesso': True,
            'estatisticas': stats
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao calcular estatísticas dos times: {str(e)}'
        }), 500


@api_bp.route('/sugerir-time-coracao', methods=['GET'])
def sugerir_time_coracao():
    """
    Sugere um time do coração baseado em estatísticas.
    
    Query params:
        estrategia: Tipo de estratégia (padrão: equilibrada)
    
    Returns:
        JSON com sugestão de time
    """
    try:
        estrategia = request.args.get('estrategia', 'equilibrada')
        time = timemania_service.sugerir_time_coracao(estrategia)
        
        return jsonify({
            'sucesso': True,
            'time': time
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao sugerir time: {str(e)}'
        }), 500


@api_bp.route('/gerar-palpite', methods=['POST'])
def gerar_palpite():
    """
    Gera palpites baseados em estratégias.
    
    Body JSON:
        estrategia: Tipo de estratégia (padrão: equilibrada)
        quantidade_numeros: Quantidade de números por jogo (padrão: 10)
        quantidade_jogos: Quantidade de jogos (padrão: 1)
    
    Returns:
        JSON com palpites gerados
    """
    try:
        data = request.get_json() or {}
        
        estrategia = data.get('estrategia', 'equilibrada')
        quantidade_numeros = data.get('quantidade_numeros', 10)
        quantidade_jogos = data.get('quantidade_jogos', 1)
        
        palpites = timemania_service.gerar_palpite(
            estrategia=estrategia,
            quantidade_numeros=quantidade_numeros,
            quantidade_jogos=quantidade_jogos
        )
        
        return jsonify({
            'sucesso': True,
            'palpites': palpites
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao gerar palpite: {str(e)}'
        }), 500


@api_bp.route('/conferir', methods=['POST'])
def conferir():
    """
    Confere um palpite com o resultado de um concurso.
    
    Body JSON:
        numeros: Lista de números apostados
        time_coracao: Time do coração escolhido
        numero_concurso: Número do concurso para conferir
    
    Returns:
        JSON com resultado da conferência
    """
    try:
        data = request.get_json() or {}
        
        numeros = data.get('numeros', [])
        time_coracao = data.get('time_coracao', '')
        numero_concurso = data.get('numero_concurso', 0)
        
        if not numeros or not time_coracao or not numero_concurso:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Parâmetros inválidos'
            }), 400
        
        resultado = timemania_service.conferir_palpite(
            numeros=numeros,
            time_coracao=time_coracao,
            numero_concurso=numero_concurso
        )
        
        return jsonify(resultado), 200 if resultado.get('sucesso') else 404
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao conferir palpite: {str(e)}'
        }), 500


@api_bp.route('/health', methods=['GET'])
def health():
    """
    Verifica o status da API.
    
    Returns:
        JSON com status da aplicação
    """
    try:
        total_concursos = resultado_model.contar_resultados()
        ultimo = resultado_model.buscar_ultimo()
        
        return jsonify({
            'sucesso': True,
            'status': 'online',
            'total_concursos': total_concursos,
            'ultimo_concurso': ultimo.get('numero') if ultimo else None
        }), 200
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'status': 'erro',
            'mensagem': str(e)
        }), 500
