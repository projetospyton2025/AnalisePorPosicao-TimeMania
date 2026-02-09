"""
Serviço para integração com a API da Caixa para obter resultados da Timemania.
"""
import requests
from typing import Dict, Optional
import config
from models.resultado_model import ResultadoModel


class ApiCaixaService:
    """
    Classe para gerenciar a comunicação com a API da Caixa.
    """
    
    def __init__(self):
        """Inicializa o serviço da API."""
        self.api_url = config.API_TIMEMANIA_URL
        self.resultado_model = ResultadoModel()
    
    def buscar_ultimo_concurso(self) -> Optional[Dict]:
        """
        Busca o último concurso da Timemania na API da Caixa.
        
        Returns:
            Dicionário com os dados do último concurso ou None em caso de erro
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Salvar no banco de dados
            if data and data.get('numero'):
                self.resultado_model.inserir(data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar último concurso: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao buscar último concurso: {e}")
            return None
    
    def buscar_concurso_especifico(self, numero: int) -> Optional[Dict]:
        """
        Busca um concurso específico da Timemania na API da Caixa.
        
        Args:
            numero: Número do concurso a ser buscado
            
        Returns:
            Dicionário com os dados do concurso ou None em caso de erro
        """
        try:
            url = f"{self.api_url}/{numero}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Salvar no banco de dados
            if data and data.get('numero'):
                self.resultado_model.inserir(data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar concurso {numero}: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado ao buscar concurso {numero}: {e}")
            return None
    
    def atualizar_base_completa(self) -> Dict[str, any]:
        """
        Atualiza a base de dados com todos os concursos disponíveis.
        Busca incrementalmente do último concurso cadastrado até o mais recente.
        
        Returns:
            Dicionário com estatísticas da atualização:
            - total_cadastrados: Total de concursos cadastrados
            - novos: Novos concursos adicionados
            - erros: Número de erros encontrados
        """
        try:
            # Buscar último concurso da API
            ultimo_api = self.buscar_ultimo_concurso()
            if not ultimo_api:
                return {
                    'sucesso': False,
                    'mensagem': 'Erro ao buscar último concurso da API',
                    'total_cadastrados': 0,
                    'novos': 0,
                    'erros': 0
                }
            
            numero_ultimo_api = ultimo_api.get('numero', 0)
            
            # Buscar último concurso do banco
            ultimo_db = self.resultado_model.buscar_ultimo()
            numero_ultimo_db = ultimo_db.get('numero', 0) if ultimo_db else 0
            
            # Se já está atualizado
            if numero_ultimo_db >= numero_ultimo_api:
                return {
                    'sucesso': True,
                    'mensagem': 'Base de dados já está atualizada',
                    'total_cadastrados': self.resultado_model.contar_resultados(),
                    'novos': 0,
                    'erros': 0
                }
            
            # Buscar concursos faltantes
            novos = 0
            erros = 0
            
            # Se não há dados no banco, buscar os últimos 100 concursos
            if numero_ultimo_db == 0:
                inicio = max(1, numero_ultimo_api - 99)
            else:
                inicio = numero_ultimo_db + 1
            
            for numero in range(inicio, numero_ultimo_api + 1):
                resultado = self.buscar_concurso_especifico(numero)
                if resultado:
                    novos += 1
                else:
                    erros += 1
            
            return {
                'sucesso': True,
                'mensagem': f'Base atualizada com sucesso',
                'total_cadastrados': self.resultado_model.contar_resultados(),
                'novos': novos,
                'erros': erros,
                'ultimo_concurso': numero_ultimo_api
            }
            
        except Exception as e:
            print(f"Erro ao atualizar base completa: {e}")
            return {
                'sucesso': False,
                'mensagem': f'Erro ao atualizar base: {str(e)}',
                'total_cadastrados': 0,
                'novos': 0,
                'erros': 0
            }
