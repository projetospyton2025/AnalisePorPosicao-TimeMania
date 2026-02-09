/**
 * JavaScript para o Sistema de Análise da Timemania
 * Gerencia interações com a API e atualizações dinâmicas
 */

// Configuração da API
const API_BASE = window.location.origin + '/api';

// Utilitários
const showLoading = (elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = '<div class="loading">Carregando</div>';
    }
};

const showError = (elementId, message) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `<div class="alert alert-error">${message}</div>`;
    }
};

const formatNumber = (num) => {
    return num.toString().padStart(2, '0');
};

const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
};

const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    const parts = dateStr.split('/');
    if (parts.length === 3) {
        return `${parts[0]}/${parts[1]}/${parts[2]}`;
    }
    return dateStr;
};

// Funções da API
async function atualizarBase() {
    try {
        const btn = document.getElementById('btn-atualizar');
        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Atualizando...';
        }
        
        const response = await fetch(`${API_BASE}/atualizar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.sucesso) {
            alert(`Base atualizada com sucesso!\n\nNovos concursos: ${data.novos}\nTotal cadastrados: ${data.total_cadastrados}`);
            location.reload();
        } else {
            alert(`Erro ao atualizar: ${data.mensagem}`);
        }
    } catch (error) {
        console.error('Erro ao atualizar base:', error);
        alert('Erro ao atualizar base de dados. Verifique o console para mais detalhes.');
    } finally {
        const btn = document.getElementById('btn-atualizar');
        if (btn) {
            btn.disabled = false;
            btn.textContent = 'Atualizar Dados';
        }
    }
}

async function carregarUltimoResultado() {
    try {
        showLoading('ultimo-resultado');
        
        const response = await fetch(`${API_BASE}/ultimo-resultado`);
        const data = await response.json();
        
        if (data.sucesso && data.resultado) {
            const resultado = data.resultado;
            const html = `
                <div class="card">
                    <h2>Último Resultado - Concurso ${resultado.numero}</h2>
                    <p><strong>Data:</strong> ${formatDate(resultado.dataApuracao)}</p>
                    <p><strong>Local:</strong> ${resultado.localSorteio || 'N/A'}</p>
                    
                    <h3 class="mt-2">Números Sorteados</h3>
                    <div class="numeros-container">
                        ${resultado.listaDezenas.map(num => `<div class="numero">${formatNumber(num)}</div>`).join('')}
                    </div>
                    
                    <div class="time-coracao mt-2">
                        <strong>Time do Coração:</strong> ${resultado.nomeTimeCoracaoMesSorte || 'N/A'}
                    </div>
                    
                    <div class="mt-2">
                        <p><strong>Acumulado:</strong> ${resultado.acumulado ? 'SIM' : 'NÃO'}</p>
                        <p><strong>Valor Arrecadado:</strong> ${formatCurrency(resultado.valorArrecadado || 0)}</p>
                        <p><strong>Próximo Concurso:</strong> ${resultado.numeroConcursoProximo || 'N/A'} - ${formatDate(resultado.dataProximoConcurso)}</p>
                        <p><strong>Prêmio Estimado:</strong> ${formatCurrency(resultado.valorEstimadoProximoConcurso || 0)}</p>
                    </div>
                </div>
            `;
            
            document.getElementById('ultimo-resultado').innerHTML = html;
        } else {
            showError('ultimo-resultado', 'Nenhum resultado encontrado. Clique em "Atualizar Dados" para buscar resultados.');
        }
    } catch (error) {
        console.error('Erro ao carregar último resultado:', error);
        showError('ultimo-resultado', 'Erro ao carregar último resultado.');
    }
}

async function carregarEstatisticas() {
    try {
        showLoading('estatisticas-gerais');
        
        const response = await fetch(`${API_BASE}/estatisticas`);
        const data = await response.json();
        
        if (data.sucesso && data.estatisticas) {
            const stats = data.estatisticas;
            
            // Estatísticas Gerais
            let html = `
                <div class="card">
                    <h2>Estatísticas Gerais</h2>
                    <div class="cards-grid">
                        <div class="stat-item">
                            <span class="stat-number">${stats.total_concursos}</span>
                            <span class="stat-label">Total de Concursos</span>
                        </div>
                    </div>
                </div>
            `;
            
            // Números Mais Frequentes
            html += `
                <div class="card">
                    <h3>Números Mais Frequentes (Top 20)</h3>
                    <div class="numeros-container">
                        ${stats.frequencia_numeros.slice(0, 20).map(item => 
                            `<div class="numero" title="Frequência: ${item.frequencia}">${formatNumber(item.numero)}</div>`
                        ).join('')}
                    </div>
                </div>
            `;
            
            // Números Mais Atrasados
            html += `
                <div class="card">
                    <h3>Números Mais Atrasados (Top 20)</h3>
                    <div class="numeros-container">
                        ${stats.atrasos.slice(0, 20).map(item => 
                            `<div class="numero" title="Atraso: ${item.atraso} concursos">${formatNumber(item.numero)}</div>`
                        ).join('')}
                    </div>
                </div>
            `;
            
            // Pares e Ímpares
            html += `
                <div class="card">
                    <h3>Distribuição Pares/Ímpares</h3>
                    <div class="cards-grid">
                        <div class="stat-item">
                            <span class="stat-number">${stats.pares_impares.percentual_pares}%</span>
                            <span class="stat-label">Pares (${stats.pares_impares.pares})</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">${stats.pares_impares.percentual_impares}%</span>
                            <span class="stat-label">Ímpares (${stats.pares_impares.impares})</span>
                        </div>
                    </div>
                </div>
            `;
            
            // Por Faixa
            html += `
                <div class="card">
                    <h3>Análise por Faixa</h3>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Faixa</th>
                                <th>Frequência</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${stats.por_faixa.map(item => `
                                <tr>
                                    <td>${item.faixa}</td>
                                    <td>${item.frequencia}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
            
            // Por Posição
            html += `
                <div class="card">
                    <h3>Análise por Posição de Sorteio</h3>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Posição</th>
                                <th>Top 10 Números</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${stats.por_posicao.map(item => `
                                <tr>
                                    <td>${item.posicao}ª</td>
                                    <td>${item.numeros.map(n => formatNumber(n.numero)).join(', ')}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
            
            // Times do Coração
            if (stats.times_coracao) {
                html += `
                    <div class="card">
                        <h3>Times do Coração Mais Sorteados (Top 10)</h3>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Time</th>
                                    <th>Frequência</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${stats.times_coracao.mais_sorteados.map(item => `
                                    <tr>
                                        <td><span class="time-coracao-badge">${item.time}</span></td>
                                        <td>${item.frequencia}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
                
                html += `
                    <div class="card">
                        <h3>Times do Coração Mais Atrasados (Top 10)</h3>
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Time</th>
                                    <th>Atraso (concursos)</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${stats.times_coracao.mais_atrasados.map(item => `
                                    <tr>
                                        <td><span class="time-coracao-badge">${item.time}</span></td>
                                        <td>${item.atraso}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }
            
            document.getElementById('estatisticas-gerais').innerHTML = html;
        } else {
            showError('estatisticas-gerais', 'Erro ao carregar estatísticas.');
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
        showError('estatisticas-gerais', 'Erro ao carregar estatísticas.');
    }
}

async function gerarPalpites() {
    try {
        const estrategia = document.getElementById('estrategia').value;
        const quantidade = parseInt(document.getElementById('quantidade-numeros').value);
        const jogos = parseInt(document.getElementById('quantidade-jogos').value);
        
        const btn = document.getElementById('btn-gerar');
        btn.disabled = true;
        btn.textContent = 'Gerando...';
        
        showLoading('resultado-palpites');
        
        const response = await fetch(`${API_BASE}/gerar-palpite`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                estrategia: estrategia,
                quantidade_numeros: quantidade,
                quantidade_jogos: jogos
            })
        });
        
        const data = await response.json();
        
        if (data.sucesso && data.palpites) {
            let html = '<div class="cards-grid">';
            
            data.palpites.forEach((palpite, index) => {
                html += `
                    <div class="card">
                        <h3>Jogo ${index + 1}</h3>
                        <p><strong>Estratégia:</strong> ${palpite.estrategia}</p>
                        <div class="numeros-container">
                            ${palpite.numeros.map(num => `<div class="numero">${formatNumber(num)}</div>`).join('')}
                        </div>
                        <div class="time-coracao mt-2">
                            <strong>Time do Coração Sugerido:</strong><br>
                            ${palpite.time_coracao.time}
                            <br><small>${palpite.time_coracao.motivo}</small>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
            document.getElementById('resultado-palpites').innerHTML = html;
        } else {
            showError('resultado-palpites', data.mensagem || 'Erro ao gerar palpites.');
        }
    } catch (error) {
        console.error('Erro ao gerar palpites:', error);
        showError('resultado-palpites', 'Erro ao gerar palpites.');
    } finally {
        const btn = document.getElementById('btn-gerar');
        btn.disabled = false;
        btn.textContent = 'Gerar Palpites';
    }
}

async function conferirPalpite() {
    try {
        const numerosInput = document.getElementById('numeros-conferir').value;
        const timeCor acao = document.getElementById('time-conferir').value;
        const concurso = parseInt(document.getElementById('concurso-conferir').value);
        
        // Validar entrada
        if (!numerosInput || !timeCoracao || !concurso) {
            alert('Por favor, preencha todos os campos.');
            return;
        }
        
        // Converter números
        const numeros = numerosInput.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));
        
        if (numeros.length < 10 || numeros.length > 15) {
            alert('Digite entre 10 e 15 números válidos separados por vírgula.');
            return;
        }
        
        const btn = document.getElementById('btn-conferir');
        btn.disabled = true;
        btn.textContent = 'Conferindo...';
        
        showLoading('resultado-conferencia');
        
        const response = await fetch(`${API_BASE}/conferir`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                numeros: numeros,
                time_coracao: timeCoracao,
                numero_concurso: concurso
            })
        });
        
        const data = await response.json();
        
        if (data.sucesso) {
            const html = `
                <div class="card">
                    <h2>Resultado da Conferência</h2>
                    <p><strong>Concurso:</strong> ${data.concurso} - ${formatDate(data.data)}</p>
                    
                    <h3 class="mt-2">Números Sorteados</h3>
                    <div class="numeros-container">
                        ${data.numeros_sorteados.map(num => {
                            const acertou = data.numeros_acertados.includes(num);
                            return `<div class="numero ${acertou ? 'acertado' : ''}">${formatNumber(num)}</div>`;
                        }).join('')}
                    </div>
                    
                    <div class="cards-grid mt-2">
                        <div class="stat-item">
                            <span class="stat-number">${data.acertos}</span>
                            <span class="stat-label">Acertos</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-number">${data.acertou_time ? 'SIM' : 'NÃO'}</span>
                            <span class="stat-label">Acertou Time</span>
                        </div>
                    </div>
                    
                    <div class="time-coracao mt-2">
                        <strong>Time Sorteado:</strong> ${data.time_sorteado}
                    </div>
                    
                    ${data.faixa_premio ? `
                        <div class="alert alert-success mt-2">
                            <strong>Parabéns!</strong> Você foi premiado na faixa: ${data.faixa_premio}
                        </div>
                    ` : (data.acertou_time ? `
                        <div class="alert alert-success mt-2">
                            <strong>Parabéns!</strong> Você acertou o Time do Coração!
                        </div>
                    ` : `
                        <div class="alert alert-info mt-2">
                            Não houve premiação neste concurso.
                        </div>
                    `)}
                </div>
            `;
            
            document.getElementById('resultado-conferencia').innerHTML = html;
        } else {
            showError('resultado-conferencia', data.mensagem || 'Erro ao conferir palpite.');
        }
    } catch (error) {
        console.error('Erro ao conferir palpite:', error);
        showError('resultado-conferencia', 'Erro ao conferir palpite.');
    } finally {
        const btn = document.getElementById('btn-conferir');
        btn.disabled = false;
        btn.textContent = 'Conferir';
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Página inicial
    if (document.getElementById('ultimo-resultado')) {
        carregarUltimoResultado();
        carregarEstatisticas();
    }
    
    // Botão de atualizar
    const btnAtualizar = document.getElementById('btn-atualizar');
    if (btnAtualizar) {
        btnAtualizar.addEventListener('click', atualizarBase);
    }
    
    // Botão de gerar palpites
    const btnGerar = document.getElementById('btn-gerar');
    if (btnGerar) {
        btnGerar.addEventListener('click', gerarPalpites);
    }
    
    // Botão de conferir
    const btnConferir = document.getElementById('btn-conferir');
    if (btnConferir) {
        btnConferir.addEventListener('click', conferirPalpite);
    }
});
