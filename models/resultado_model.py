"""
Model para armazenar e gerenciar resultados da Timemania no banco de dados SQLite.
"""
import sqlite3
import json
from typing import List, Dict, Optional
import config


class ResultadoModel:
    """
    Classe para gerenciar resultados da Timemania no banco de dados SQLite.
    """
    
    def __init__(self):
        """Inicializa o modelo e cria a tabela se não existir."""
        self.db_path = config.DATABASE_PATH
        self._criar_tabela()
    
    def _criar_tabela(self):
        """Cria a tabela de resultados se não existir."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resultados (
                numero INTEGER PRIMARY KEY,
                acumulado BOOLEAN,
                dataApuracao TEXT,
                dataProximoConcurso TEXT,
                dezenasSorteadasOrdemSorteio TEXT,
                exibirDetalhamentoPorCidade BOOLEAN,
                indicadorConcursoEspecial INTEGER,
                listaDezenas TEXT,
                listaDezenasSegundoSorteio TEXT,
                listaMunicipioUFGanhadores TEXT,
                listaRateioPremio TEXT,
                localSorteio TEXT,
                nomeMunicipioUFSorteio TEXT,
                nomeTimeCoracaoMesSorte TEXT,
                time_coracao_nome TEXT,
                time_coracao_numero INTEGER,
                numeroConcursoAnterior INTEGER,
                numeroConcursoFinal_0_5 INTEGER,
                numeroConcursoProximo INTEGER,
                numeroJogo INTEGER,
                tipoJogo TEXT,
                valorArrecadado REAL,
                valorAcumuladoConcurso_0_5 REAL,
                valorAcumuladoProximoConcurso REAL,
                valorEstimadoProximoConcurso REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def inserir(self, resultado: Dict) -> bool:
        """
        Insere ou atualiza um resultado no banco de dados.
        
        Args:
            resultado: Dicionário com os dados do resultado da API
            
        Returns:
            True se a operação foi bem-sucedida, False caso contrário
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Extrair time do coração
            time_coracao_nome = resultado.get('nomeTimeCoracaoMesSorte', '')
            time_coracao_numero = self._extrair_numero_time(time_coracao_nome)
            
            cursor.execute('''
                INSERT OR REPLACE INTO resultados (
                    numero, acumulado, dataApuracao, dataProximoConcurso,
                    dezenasSorteadasOrdemSorteio, exibirDetalhamentoPorCidade,
                    indicadorConcursoEspecial, listaDezenas, listaDezenasSegundoSorteio,
                    listaMunicipioUFGanhadores, listaRateioPremio, localSorteio,
                    nomeMunicipioUFSorteio, nomeTimeCoracaoMesSorte, time_coracao_nome,
                    time_coracao_numero, numeroConcursoAnterior, numeroConcursoFinal_0_5,
                    numeroConcursoProximo, numeroJogo, tipoJogo, valorArrecadado,
                    valorAcumuladoConcurso_0_5, valorAcumuladoProximoConcurso,
                    valorEstimadoProximoConcurso
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                resultado.get('numero'),
                resultado.get('acumulado'),
                resultado.get('dataApuracao'),
                resultado.get('dataProximoConcurso'),
                json.dumps(resultado.get('dezenasSorteadasOrdemSorteio', [])),
                resultado.get('exibirDetalhamentoPorCidade'),
                resultado.get('indicadorConcursoEspecial'),
                json.dumps(resultado.get('listaDezenas', [])),
                json.dumps(resultado.get('listaDezenasSegundoSorteio')),
                json.dumps(resultado.get('listaMunicipioUFGanhadores', [])),
                json.dumps(resultado.get('listaRateioPremio', [])),
                resultado.get('localSorteio'),
                resultado.get('nomeMunicipioUFSorteio'),
                resultado.get('nomeTimeCoracaoMesSorte'),
                time_coracao_nome,
                time_coracao_numero,
                resultado.get('numeroConcursoAnterior'),
                resultado.get('numeroConcursoFinal_0_5'),
                resultado.get('numeroConcursoProximo'),
                resultado.get('numeroJogo'),
                resultado.get('tipoJogo'),
                resultado.get('valorArrecadado'),
                resultado.get('valorAcumuladoConcurso_0_5'),
                resultado.get('valorAcumuladoProximoConcurso'),
                resultado.get('valorEstimadoProximoConcurso')
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao inserir resultado: {e}")
            return False
    
    def buscar_ultimo(self) -> Optional[Dict]:
        """
        Busca o último resultado cadastrado.
        
        Returns:
            Dicionário com o último resultado ou None se não houver dados
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM resultados ORDER BY numero DESC LIMIT 1')
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return self._row_to_dict(row)
            return None
            
        except Exception as e:
            print(f"Erro ao buscar último resultado: {e}")
            return None
    
    def buscar_todos(self, limite: Optional[int] = None) -> List[Dict]:
        """
        Busca todos os resultados cadastrados.
        
        Args:
            limite: Quantidade máxima de resultados (None para todos)
            
        Returns:
            Lista de dicionários com os resultados
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if limite:
                cursor.execute('SELECT * FROM resultados ORDER BY numero DESC LIMIT ?', (limite,))
            else:
                cursor.execute('SELECT * FROM resultados ORDER BY numero DESC')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._row_to_dict(row) for row in rows]
            
        except Exception as e:
            print(f"Erro ao buscar resultados: {e}")
            return []
    
    def buscar_por_numero(self, numero: int) -> Optional[Dict]:
        """
        Busca um resultado específico pelo número do concurso.
        
        Args:
            numero: Número do concurso
            
        Returns:
            Dicionário com o resultado ou None se não encontrado
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM resultados WHERE numero = ?', (numero,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return self._row_to_dict(row)
            return None
            
        except Exception as e:
            print(f"Erro ao buscar resultado: {e}")
            return None
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """
        Converte uma linha do banco em dicionário.
        
        Args:
            row: Linha do banco de dados
            
        Returns:
            Dicionário com os dados do resultado
        """
        result = dict(row)
        
        # Converter JSON strings de volta para listas/objetos
        json_fields = [
            'dezenasSorteadasOrdemSorteio',
            'listaDezenas',
            'listaDezenasSegundoSorteio',
            'listaMunicipioUFGanhadores',
            'listaRateioPremio'
        ]
        
        for field in json_fields:
            if result.get(field):
                try:
                    result[field] = json.loads(result[field])
                except:
                    result[field] = []
        
        return result
    
    def _extrair_numero_time(self, nome_time: str) -> Optional[int]:
        """
        Extrai o número do time a partir do nome completo.
        
        Args:
            nome_time: Nome completo do time (ex: "VILA NOVA        GO")
            
        Returns:
            Número do time (1-80) ou None se não puder ser determinado
        """
        # TODO: Implementar mapeamento de times quando disponível
        # Por enquanto, retorna None
        return None
    
    def contar_resultados(self) -> int:
        """
        Conta o total de resultados cadastrados.
        
        Returns:
            Número total de resultados
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM resultados')
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
            
        except Exception as e:
            print(f"Erro ao contar resultados: {e}")
            return 0
