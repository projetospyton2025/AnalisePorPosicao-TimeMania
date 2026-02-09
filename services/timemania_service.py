"""
Serviço para geração de palpites da Timemania usando estatísticas.
"""
import random
from typing import List, Dict, Set
import config
from services.estatistica_service import EstatisticaService


class TimemaniaService:
    """
    Classe para gerar palpites baseados em estratégias estatísticas.
    """
    
    def __init__(self):
        """Inicializa o serviço de palpites."""
        self.estatistica_service = EstatisticaService()
    
    def gerar_palpite(
        self,
        estrategia: str = 'equilibrada',
        quantidade_numeros: int = 10,
        quantidade_jogos: int = 1
    ) -> List[Dict]:
        """
        Gera palpites baseados na estratégia escolhida.
        
        Args:
            estrategia: Tipo de estratégia ('equilibrada', 'agressiva', etc.)
            quantidade_numeros: Quantidade de números por jogo (10-15)
            quantidade_jogos: Quantidade de jogos a gerar (1-100)
            
        Returns:
            Lista de jogos com números e time sugerido
        """
        # Validar parâmetros
        if quantidade_numeros < config.MIN_JOGO or quantidade_numeros > config.MAX_JOGO:
            quantidade_numeros = config.MIN_JOGO
        
        if quantidade_jogos < 1 or quantidade_jogos > 100:
            quantidade_jogos = 1
        
        if estrategia not in config.ESTRATEGIAS:
            estrategia = 'equilibrada'
        
        # Gerar jogos
        jogos = []
        for _ in range(quantidade_jogos):
            numeros = self._gerar_numeros_por_estrategia(estrategia, quantidade_numeros)
            time = self.sugerir_time_coracao(estrategia)
            
            jogos.append({
                'numeros': sorted(numeros),
                'time_coracao': time,
                'estrategia': estrategia,
                'quantidade': quantidade_numeros
            })
        
        return jogos
    
    def _gerar_numeros_por_estrategia(
        self,
        estrategia: str,
        quantidade: int
    ) -> List[int]:
        """
        Gera números baseados na estratégia específica.
        
        Args:
            estrategia: Nome da estratégia
            quantidade: Quantidade de números a gerar
            
        Returns:
            Lista de números gerados
        """
        if estrategia == 'equilibrada':
            return self._estrategia_equilibrada(quantidade)
        elif estrategia == 'agressiva':
            return self._estrategia_agressiva(quantidade)
        elif estrategia == 'conservadora':
            return self._estrategia_conservadora(quantidade)
        elif estrategia == 'mista':
            return self._estrategia_mista(quantidade)
        elif estrategia == 'atrasados':
            return self._estrategia_atrasados(quantidade)
        elif estrategia == 'por_faixa':
            return self._estrategia_por_faixa(quantidade)
        elif estrategia == 'por_posicao':
            return self._estrategia_por_posicao(quantidade)
        else:
            return self._estrategia_equilibrada(quantidade)
    
    def _estrategia_equilibrada(self, quantidade: int) -> List[int]:
        """
        Estratégia equilibrada: Mix de números frequentes e atrasados.
        50% frequentes, 50% atrasados.
        """
        frequentes = self.estatistica_service.obter_numeros_mais_frequentes(40)
        atrasados = self.estatistica_service.obter_numeros_mais_atrasados(40)
        
        metade = quantidade // 2
        numeros = set()
        
        # Adicionar metade de frequentes
        numeros.update(random.sample(frequentes[:20], min(metade, len(frequentes[:20]))))
        
        # Completar com atrasados
        while len(numeros) < quantidade:
            candidatos = [n for n in atrasados if n not in numeros]
            if candidatos:
                numeros.add(random.choice(candidatos[:20]))
            else:
                # Se não houver mais candidatos, adicionar aleatório
                todos = list(range(1, config.MAX_NUMEROS + 1))
                disponiveis = [n for n in todos if n not in numeros]
                if disponiveis:
                    numeros.add(random.choice(disponiveis))
                else:
                    break
        
        return list(numeros)
    
    def _estrategia_agressiva(self, quantidade: int) -> List[int]:
        """
        Estratégia agressiva: Prioriza números mais frequentes.
        80% frequentes, 20% outros.
        """
        frequentes = self.estatistica_service.obter_numeros_mais_frequentes(40)
        
        quantidade_frequentes = int(quantidade * 0.8)
        numeros = set()
        
        # Adicionar números frequentes
        numeros.update(random.sample(
            frequentes[:30],
            min(quantidade_frequentes, len(frequentes[:30]))
        ))
        
        # Completar com números aleatórios
        while len(numeros) < quantidade:
            todos = list(range(1, config.MAX_NUMEROS + 1))
            disponiveis = [n for n in todos if n not in numeros]
            if disponiveis:
                numeros.add(random.choice(disponiveis))
            else:
                break
        
        return list(numeros)
    
    def _estrategia_conservadora(self, quantidade: int) -> List[int]:
        """
        Estratégia conservadora: Prioriza números atrasados.
        80% atrasados, 20% outros.
        """
        atrasados = self.estatistica_service.obter_numeros_mais_atrasados(40)
        
        quantidade_atrasados = int(quantidade * 0.8)
        numeros = set()
        
        # Adicionar números atrasados
        numeros.update(random.sample(
            atrasados[:30],
            min(quantidade_atrasados, len(atrasados[:30]))
        ))
        
        # Completar com números aleatórios
        while len(numeros) < quantidade:
            todos = list(range(1, config.MAX_NUMEROS + 1))
            disponiveis = [n for n in todos if n not in numeros]
            if disponiveis:
                numeros.add(random.choice(disponiveis))
            else:
                break
        
        return list(numeros)
    
    def _estrategia_mista(self, quantidade: int) -> List[int]:
        """
        Estratégia mista: Combina múltiplas estratégias.
        40% frequentes, 40% atrasados, 20% aleatórios.
        """
        frequentes = self.estatistica_service.obter_numeros_mais_frequentes(30)
        atrasados = self.estatistica_service.obter_numeros_mais_atrasados(30)
        
        qtd_frequentes = int(quantidade * 0.4)
        qtd_atrasados = int(quantidade * 0.4)
        
        numeros = set()
        
        # Adicionar frequentes
        numeros.update(random.sample(
            frequentes[:20],
            min(qtd_frequentes, len(frequentes[:20]))
        ))
        
        # Adicionar atrasados
        candidatos_atrasados = [n for n in atrasados[:20] if n not in numeros]
        if candidatos_atrasados:
            numeros.update(random.sample(
                candidatos_atrasados,
                min(qtd_atrasados, len(candidatos_atrasados))
            ))
        
        # Completar com aleatórios
        while len(numeros) < quantidade:
            todos = list(range(1, config.MAX_NUMEROS + 1))
            disponiveis = [n for n in todos if n not in numeros]
            if disponiveis:
                numeros.add(random.choice(disponiveis))
            else:
                break
        
        return list(numeros)
    
    def _estrategia_atrasados(self, quantidade: int) -> List[int]:
        """
        Estratégia focada em atrasados: Apenas números com maior atraso.
        """
        atrasados = self.estatistica_service.obter_numeros_mais_atrasados(quantidade * 2)
        return random.sample(atrasados[:quantidade * 2], min(quantidade, len(atrasados)))
    
    def _estrategia_por_faixa(self, quantidade: int) -> List[int]:
        """
        Estratégia por faixa: Distribui números uniformemente pelas faixas.
        """
        # 8 faixas de 10 números cada (01-10, 11-20, ..., 71-80)
        faixas = [list(range(i, i + 10)) for i in range(1, 81, 10)]
        
        numeros = set()
        numeros_por_faixa = quantidade // 8
        resto = quantidade % 8
        
        # Distribuir uniformemente
        for i, faixa in enumerate(faixas):
            qtd = numeros_por_faixa + (1 if i < resto else 0)
            if qtd > 0:
                numeros.update(random.sample(faixa, min(qtd, len(faixa))))
        
        # Se ainda faltam números, completar aleatoriamente
        while len(numeros) < quantidade:
            todos = list(range(1, config.MAX_NUMEROS + 1))
            disponiveis = [n for n in todos if n not in numeros]
            if disponiveis:
                numeros.add(random.choice(disponiveis))
            else:
                break
        
        return list(numeros)
    
    def _estrategia_por_posicao(self, quantidade: int) -> List[int]:
        """
        Estratégia por posição: Usa análise posicional do sorteio.
        Seleciona números mais frequentes em cada posição.
        """
        por_posicao = self.estatistica_service.calcular_por_posicao_sorteio()
        
        numeros = set()
        
        # Tentar pegar pelo menos um número de cada posição
        for posicao_data in por_posicao[:quantidade]:
            if len(numeros) >= quantidade:
                break
            
            numeros_posicao = posicao_data.get('numeros', [])
            if numeros_posicao:
                # Escolher aleatoriamente entre os top 3 dessa posição
                candidatos = [n['numero'] for n in numeros_posicao[:3] if n['numero'] not in numeros]
                if candidatos:
                    numeros.add(random.choice(candidatos))
        
        # Completar se necessário
        if len(numeros) < quantidade:
            frequentes = self.estatistica_service.obter_numeros_mais_frequentes(40)
            candidatos = [n for n in frequentes if n not in numeros]
            while len(numeros) < quantidade and candidatos:
                numeros.add(candidatos.pop(0))
        
        return list(numeros)
    
    def sugerir_time_coracao(self, estrategia: str = 'equilibrada') -> Dict:
        """
        Sugere um time do coração baseado em estatísticas.
        
        Args:
            estrategia: Tipo de estratégia para sugerir o time
            
        Returns:
            Dicionário com informações do time sugerido
        """
        if estrategia == 'agressiva':
            # Time mais sorteado recentemente
            times = self.estatistica_service.calcular_times_mais_sorteados(10)
            if times:
                time_escolhido = random.choice(times[:3])  # Top 3
                return {
                    'time': time_escolhido['time'],
                    'motivo': 'Time mais sorteado recentemente',
                    'frequencia': time_escolhido['frequencia']
                }
        
        elif estrategia == 'conservadora':
            # Time mais atrasado
            times = self.estatistica_service.calcular_times_mais_atrasados(10)
            if times:
                time_escolhido = random.choice(times[:3])  # Top 3 atrasados
                return {
                    'time': time_escolhido['time'],
                    'motivo': 'Time mais atrasado',
                    'atraso': time_escolhido['atraso']
                }
        
        else:
            # Equilibrada ou outras: escolher aleatoriamente com peso
            todos_times = self.estatistica_service.calcular_frequencia_times_coracao()
            if todos_times:
                # Escolher aleatoriamente entre times com frequência mediana
                meio = len(todos_times) // 2
                candidatos = todos_times[meio - 5:meio + 5] if len(todos_times) > 10 else todos_times
                if candidatos:
                    time_escolhido = random.choice(candidatos)
                    return {
                        'time': time_escolhido['time'],
                        'motivo': 'Time com frequência equilibrada',
                        'frequencia': time_escolhido['frequencia']
                    }
        
        # Fallback: retornar time aleatório
        todos_times = self.estatistica_service.calcular_frequencia_times_coracao()
        if todos_times:
            time_escolhido = random.choice(todos_times)
            return {
                'time': time_escolhido['time'],
                'motivo': 'Time escolhido aleatoriamente',
                'frequencia': time_escolhido.get('frequencia', 0)
            }
        
        return {
            'time': 'Não disponível',
            'motivo': 'Sem dados suficientes',
            'frequencia': 0
        }
    
    def conferir_palpite(
        self,
        numeros: List[int],
        time_coracao: str,
        numero_concurso: int
    ) -> Dict:
        """
        Confere um palpite com o resultado de um concurso.
        
        Args:
            numeros: Lista de números do palpite
            time_coracao: Time do coração escolhido
            numero_concurso: Número do concurso para conferir
            
        Returns:
            Dicionário com resultado da conferência
        """
        from models.resultado_model import ResultadoModel
        
        resultado_model = ResultadoModel()
        resultado = resultado_model.buscar_por_numero(numero_concurso)
        
        if not resultado:
            return {
                'sucesso': False,
                'mensagem': 'Concurso não encontrado'
            }
        
        # Conferir números
        numeros_sorteados = [int(n) for n in resultado.get('listaDezenas', [])]
        acertos = len(set(numeros) & set(numeros_sorteados))
        
        # Conferir time
        time_sorteado = resultado.get('nomeTimeCoracaoMesSorte', '')
        acertou_time = time_coracao.strip().upper() == time_sorteado.strip().upper()
        
        # Determinar premiação
        faixa_premio = None
        if acertos == 7:
            faixa_premio = '7 acertos'
        elif acertos == 6:
            faixa_premio = '6 acertos'
        elif acertos == 5:
            faixa_premio = '5 acertos'
        elif acertos == 4:
            faixa_premio = '4 acertos'
        elif acertos == 3:
            faixa_premio = '3 acertos'
        
        return {
            'sucesso': True,
            'concurso': numero_concurso,
            'data': resultado.get('dataApuracao'),
            'acertos': acertos,
            'numeros_sorteados': numeros_sorteados,
            'numeros_acertados': list(set(numeros) & set(numeros_sorteados)),
            'acertou_time': acertou_time,
            'time_sorteado': time_sorteado,
            'faixa_premio': faixa_premio,
            'premiado': acertos >= 3 or acertou_time
        }
