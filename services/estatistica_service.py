"""
Serviço para cálculos estatísticos dos resultados da Timemania.
"""
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import config
from models.resultado_model import ResultadoModel


class EstatisticaService:
    """
    Classe para calcular estatísticas dos resultados da Timemania.
    """
    
    def __init__(self):
        """Inicializa o serviço de estatísticas."""
        self.resultado_model = ResultadoModel()
    
    def calcular_estatisticas_completas(self) -> Dict:
        """
        Calcula todas as estatísticas disponíveis.
        
        Returns:
            Dicionário com todas as estatísticas
        """
        return {
            'total_concursos': self.resultado_model.contar_resultados(),
            'frequencia_numeros': self.calcular_frequencia_numeros(),
            'atrasos': self.calcular_atrasos(),
            'pares_impares': self.calcular_pares_impares(),
            'por_faixa': self.calcular_por_faixa(),
            'por_digito': self.calcular_por_digito(),
            'por_posicao': self.calcular_por_posicao_sorteio(),
            'times_coracao': {
                'frequencia': self.calcular_frequencia_times_coracao(),
                'mais_sorteados': self.calcular_times_mais_sorteados(),
                'mais_atrasados': self.calcular_times_mais_atrasados()
            }
        }
    
    def calcular_frequencia_numeros(self) -> List[Dict]:
        """
        Calcula a frequência de cada número (01-80).
        
        Returns:
            Lista ordenada por frequência decrescente com {numero, frequencia}
        """
        resultados = self.resultado_model.buscar_todos()
        contador = Counter()
        
        for resultado in resultados:
            dezenas = resultado.get('listaDezenas', [])
            for dezena in dezenas:
                numero = int(dezena)
                contador[numero] += 1
        
        # Garantir que todos os números de 1 a 80 estejam presentes
        for i in range(1, config.MAX_NUMEROS + 1):
            if i not in contador:
                contador[i] = 0
        
        # Ordenar por frequência decrescente
        frequencias = [
            {'numero': num, 'frequencia': freq}
            for num, freq in contador.most_common()
        ]
        
        return frequencias
    
    def calcular_atrasos(self) -> List[Dict]:
        """
        Calcula o atraso de cada número (concursos sem aparecer).
        
        Returns:
            Lista ordenada por atraso decrescente com {numero, atraso}
        """
        resultados = self.resultado_model.buscar_todos()
        if not resultados:
            return []
        
        # Inicializar atrasos com valor alto
        atrasos = {i: len(resultados) for i in range(1, config.MAX_NUMEROS + 1)}
        
        # Percorrer resultados do mais recente ao mais antigo
        for idx, resultado in enumerate(resultados):
            dezenas = resultado.get('listaDezenas', [])
            for dezena in dezenas:
                numero = int(dezena)
                # Atualizar apenas se ainda não foi encontrado (mais recente)
                if atrasos[numero] == len(resultados):
                    atrasos[numero] = idx
        
        # Converter para lista ordenada
        lista_atrasos = [
            {'numero': num, 'atraso': atraso}
            for num, atraso in sorted(atrasos.items(), key=lambda x: x[1], reverse=True)
        ]
        
        return lista_atrasos
    
    def calcular_pares_impares(self) -> Dict:
        """
        Calcula a distribuição de números pares e ímpares.
        
        Returns:
            Dicionário com contagens e percentuais de pares/ímpares
        """
        resultados = self.resultado_model.buscar_todos()
        total_pares = 0
        total_impares = 0
        
        for resultado in resultados:
            dezenas = resultado.get('listaDezenas', [])
            for dezena in dezenas:
                numero = int(dezena)
                if numero % 2 == 0:
                    total_pares += 1
                else:
                    total_impares += 1
        
        total = total_pares + total_impares
        
        return {
            'pares': total_pares,
            'impares': total_impares,
            'percentual_pares': round(total_pares / total * 100, 2) if total > 0 else 0,
            'percentual_impares': round(total_impares / total * 100, 2) if total > 0 else 0
        }
    
    def calcular_por_faixa(self) -> List[Dict]:
        """
        Calcula a frequência de números por faixa de dezenas.
        Faixas: 01-10, 11-20, 21-30, 31-40, 41-50, 51-60, 61-70, 71-80
        
        Returns:
            Lista com frequência por faixa
        """
        resultados = self.resultado_model.buscar_todos()
        faixas = {
            '01-10': 0, '11-20': 0, '21-30': 0, '31-40': 0,
            '41-50': 0, '51-60': 0, '61-70': 0, '71-80': 0
        }
        
        for resultado in resultados:
            dezenas = resultado.get('listaDezenas', [])
            for dezena in dezenas:
                numero = int(dezena)
                if 1 <= numero <= 10:
                    faixas['01-10'] += 1
                elif 11 <= numero <= 20:
                    faixas['11-20'] += 1
                elif 21 <= numero <= 30:
                    faixas['21-30'] += 1
                elif 31 <= numero <= 40:
                    faixas['31-40'] += 1
                elif 41 <= numero <= 50:
                    faixas['41-50'] += 1
                elif 51 <= numero <= 60:
                    faixas['51-60'] += 1
                elif 61 <= numero <= 70:
                    faixas['61-70'] += 1
                elif 71 <= numero <= 80:
                    faixas['71-80'] += 1
        
        return [
            {'faixa': faixa, 'frequencia': freq}
            for faixa, freq in faixas.items()
        ]
    
    def calcular_por_digito(self) -> List[Dict]:
        """
        Calcula a frequência por dígito final (0-9).
        
        Returns:
            Lista com frequência por dígito
        """
        resultados = self.resultado_model.buscar_todos()
        digitos = {i: 0 for i in range(10)}
        
        for resultado in resultados:
            dezenas = resultado.get('listaDezenas', [])
            for dezena in dezenas:
                numero = int(dezena)
                digito = numero % 10
                digitos[digito] += 1
        
        return [
            {'digito': dig, 'frequencia': freq}
            for dig, freq in sorted(digitos.items())
        ]
    
    def calcular_por_posicao_sorteio(self) -> List[Dict]:
        """
        Analisa a frequência de cada número em cada posição do sorteio (1ª a 7ª).
        
        Returns:
            Lista com frequência por posição e número
        """
        resultados = self.resultado_model.buscar_todos()
        
        # Dicionário: posicao -> numero -> frequencia
        posicoes = {i: Counter() for i in range(1, 8)}
        
        for resultado in resultados:
            dezenas_ordem = resultado.get('dezenasSorteadasOrdemSorteio', [])
            for idx, dezena in enumerate(dezenas_ordem[:7], start=1):
                numero = int(dezena)
                posicoes[idx][numero] += 1
        
        # Converter para formato de retorno
        resultado_posicoes = []
        for posicao in range(1, 8):
            numeros_freq = [
                {'numero': num, 'frequencia': freq}
                for num, freq in posicoes[posicao].most_common(10)  # Top 10 por posição
            ]
            resultado_posicoes.append({
                'posicao': posicao,
                'numeros': numeros_freq
            })
        
        return resultado_posicoes
    
    def calcular_frequencia_times_coracao(self) -> List[Dict]:
        """
        Calcula a frequência de cada time do coração.
        
        Returns:
            Lista ordenada por frequência com {time, frequencia}
        """
        resultados = self.resultado_model.buscar_todos()
        contador = Counter()
        
        for resultado in resultados:
            time = resultado.get('nomeTimeCoracaoMesSorte', '')
            if time:
                contador[time] += 1
        
        return [
            {'time': time, 'frequencia': freq}
            for time, freq in contador.most_common()
        ]
    
    def calcular_times_mais_sorteados(self, limite: int = 10) -> List[Dict]:
        """
        Retorna os times do coração mais sorteados.
        
        Args:
            limite: Quantidade de times a retornar (padrão: 10)
            
        Returns:
            Lista dos times mais sorteados
        """
        frequencia = self.calcular_frequencia_times_coracao()
        return frequencia[:limite]
    
    def calcular_times_mais_atrasados(self, limite: int = 10) -> List[Dict]:
        """
        Calcula os times do coração com maior atraso (mais tempo sem serem sorteados).
        
        Args:
            limite: Quantidade de times a retornar (padrão: 10)
            
        Returns:
            Lista dos times mais atrasados
        """
        resultados = self.resultado_model.buscar_todos()
        if not resultados:
            return []
        
        # Mapear último concurso de cada time
        ultimos = {}
        todos_times = set()
        
        for idx, resultado in enumerate(resultados):
            time = resultado.get('nomeTimeCoracaoMesSorte', '')
            if time:
                todos_times.add(time)
                if time not in ultimos:
                    ultimos[time] = idx
        
        # Calcular atrasos
        atrasos = []
        for time in todos_times:
            atraso = ultimos.get(time, len(resultados))
            atrasos.append({'time': time, 'atraso': atraso})
        
        # Ordenar por atraso decrescente
        atrasos.sort(key=lambda x: x['atraso'], reverse=True)
        
        return atrasos[:limite]
    
    def obter_numeros_mais_frequentes(self, limite: int = 20) -> List[int]:
        """
        Retorna os números mais frequentes.
        
        Args:
            limite: Quantidade de números a retornar
            
        Returns:
            Lista dos números mais frequentes
        """
        frequencias = self.calcular_frequencia_numeros()
        return [item['numero'] for item in frequencias[:limite]]
    
    def obter_numeros_mais_atrasados(self, limite: int = 20) -> List[int]:
        """
        Retorna os números mais atrasados.
        
        Args:
            limite: Quantidade de números a retornar
            
        Returns:
            Lista dos números mais atrasados
        """
        atrasos = self.calcular_atrasos()
        return [item['numero'] for item in atrasos[:limite]]
