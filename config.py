"""
Configurações e constantes do sistema de análise da Timemania.
"""
import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Configurações do Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'timemania-secret-key-2025')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5058))

# Configurações do Banco de Dados
DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'database.db'))

# API da Caixa
API_TIMEMANIA_URL = os.getenv(
    'API_TIMEMANIA_URL',
    'https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania'
)

# Constantes da Timemania
MIN_NUMEROS = 1
MAX_NUMEROS = 80
NUMEROS_SORTEADOS = 7
MIN_JOGO = 10
MAX_JOGO = 15
TOTAL_TIMES = 80

# Identidade Visual da Timemania
COR_PRINCIPAL_AMARELO = '#FFF600'
COR_SECUNDARIA_VERDE = '#12923D'

# Paleta Amarela (0% a 100%)
PALETA_AMARELA = {
    100: '#ffffff',
    95: '#fffee6',
    90: '#fffdcc',
    85: '#fffcb3',
    80: '#fffc99',
    75: '#fffb80',
    70: '#fffa66',
    65: '#fff94d',
    60: '#fff833',
    55: '#fff71a',
    50: '#FFF600',  # Cor principal
    45: '#e6de00',
    40: '#ccc500',
    35: '#b3ad00',
    30: '#999400',
    25: '#807b00',
    20: '#666300',
    15: '#4d4a00',
    10: '#333100',
    5: '#1a1900',
    0: '#000000'
}

# Paleta Verde (0% a 100%)
PALETA_VERDE = {
    100: '#ffffff',
    95: '#e8fcef',
    90: '#d2f9df',
    85: '#bbf7cf',
    80: '#a4f4bf',
    75: '#8ef1af',
    70: '#77ee9f',
    65: '#60eb8f',
    60: '#49e97e',
    55: '#33e66e',
    50: '#1ce35e',
    45: '#19cc55',
    40: '#16b64b',
    35: '#149f42',
    32: '#12923D',  # Cor secundária
    30: '#118839',
    25: '#0e712f',
    20: '#0b5b26',
    15: '#08441c',
    10: '#062d13',
    5: '#031709',
    0: '#000000'
}

# Logo da Timemania
LOGO_URL = 'https://i.postimg.cc/W4g9ShFc/timemania.png'

# Estratégias de palpites
ESTRATEGIAS = [
    'equilibrada',
    'agressiva',
    'conservadora',
    'mista',
    'atrasados',
    'por_faixa',
    'por_posicao'
]
