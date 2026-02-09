# Sistema de Análise por Posição - TIMEMANIA

Sistema completo de análise estatística e geração de palpites para a loteria TIMEMANIA da Caixa Econômica Federal.

![Timemania Logo](https://i.postimg.cc/W4g9ShFc/timemania.png)

## 📋 Sobre a TIMEMANIA

A TIMEMANIA é uma modalidade de loteria da Caixa Econômica Federal que combina:
- **7 números sorteados** de 01 a 80
- **1 Time do Coração** entre 80 times de futebol cadastrados

### Características
- **Números disponíveis**: 01 a 80
- **Números sorteados**: 7 por concurso
- **Jogo mínimo**: 10 números
- **Jogo máximo**: 15 números
- **Time do Coração**: Escolha obrigatória de um dos 80 times

### Premiação
1. **7 acertos** - Prêmio principal
2. **6 acertos** - Segunda faixa
3. **5 acertos** - Terceira faixa
4. **4 acertos** - Quarta faixa
5. **3 acertos** - Quinta faixa
6. **Time do Coração** - Sexta faixa (independente dos acertos nos números)

## 🎨 Identidade Visual

O sistema utiliza as cores oficiais da TIMEMANIA:
- **Amarelo #FFF600** - Cor principal para números
- **Verde #12923D** - Cor secundária para Time do Coração

## ⚡ Características do Sistema

### ✅ Integração com API Oficial
- Consome dados reais da API da Caixa
- Atualização automática de resultados
- Dados históricos completos

### 📊 Análises Estatísticas Completas
- Frequência de cada número (01-80)
- Números mais atrasados
- Distribuição pares/ímpares
- Análise por faixa de dezenas
- Análise por dígito final
- **Análise posicional** (1ª a 7ª posição do sorteio)
- Estatísticas dos Times do Coração

### 🎯 Geração Inteligente de Palpites

7 estratégias diferentes:

1. **Equilibrada** - Mix de números frequentes (50%) e atrasados (50%)
2. **Agressiva** - Prioriza números mais frequentes (80%)
3. **Conservadora** - Prioriza números atrasados (80%)
4. **Mista** - Combina múltiplas abordagens (40% frequentes, 40% atrasados, 20% aleatórios)
5. **Atrasados** - Foca apenas em números com maior atraso
6. **Por Faixa** - Distribui números uniformemente por faixas
7. **Por Posição** - Usa análise posicional do sorteio

### 🏆 Sugestão de Time do Coração
- Baseada em frequência histórica
- Times mais sorteados
- Times mais atrasados
- Sugestão automática por estratégia

### ✅ Conferência de Palpites
- Confira seus números com qualquer concurso
- Verifica acertos e premiação
- Confere Time do Coração

## 🚀 Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/projetospyton2025/AnalisePorPosicao-TimeMania.git
cd AnalisePorPosicao-TimeMania
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente (opcional):**
```bash
cp .env.example .env
# Edite o arquivo .env se necessário
```

4. **Inicie o servidor:**
```bash
python app.py
```

5. **Acesse no navegador:**
```
http://localhost:5058
```

## 📖 Como Usar

### 1. Atualizar Base de Dados
Ao iniciar pela primeira vez, clique em "Atualizar Dados" no menu para baixar os resultados históricos da API da Caixa.

### 2. Visualizar Estatísticas
Na página inicial, você encontra:
- Último resultado sorteado
- Estatísticas gerais
- Números mais frequentes
- Números mais atrasados
- Análise por posição
- Estatísticas dos Times do Coração

### 3. Gerar Palpites
Na página "Gerar Palpites":
1. Escolha uma estratégia
2. Defina a quantidade de números (10-15)
3. Defina quantos jogos deseja gerar
4. Clique em "Gerar Palpites"
5. O sistema sugere automaticamente um Time do Coração

### 4. Conferir Palpite
Para conferir um palpite:
1. Digite seus números (separados por vírgula)
2. Digite o Time do Coração
3. Digite o número do concurso
4. Clique em "Conferir"
5. Veja os acertos e se foi premiado

## 🔌 API REST

### Endpoints Disponíveis

#### Atualizar Base de Dados
```http
POST /api/atualizar
```
Atualiza a base com os concursos mais recentes.

#### Último Resultado
```http
GET /api/ultimo-resultado
```
Retorna o último concurso cadastrado.

#### Listar Resultados
```http
GET /api/resultados?limite=100
```
Lista resultados com paginação opcional.

#### Resultado Específico
```http
GET /api/resultado/{numero}
```
Busca um concurso específico.

#### Estatísticas Completas
```http
GET /api/estatisticas
```
Retorna todas as estatísticas calculadas.

#### Estatísticas dos Times
```http
GET /api/estatisticas/times-coracao
```
Retorna estatísticas específicas dos Times do Coração.

#### Sugerir Time do Coração
```http
GET /api/sugerir-time-coracao?estrategia=equilibrada
```
Sugere um Time do Coração baseado na estratégia.

#### Gerar Palpite
```http
POST /api/gerar-palpite
Content-Type: application/json

{
  "estrategia": "equilibrada",
  "quantidade_numeros": 10,
  "quantidade_jogos": 3
}
```

#### Conferir Palpite
```http
POST /api/conferir
Content-Type: application/json

{
  "numeros": [5, 12, 23, 34, 45, 56, 67, 78, 11, 22],
  "time_coracao": "SÃO PAULO SP",
  "numero_concurso": 2277
}
```

## 📁 Estrutura do Projeto

```
AnalisePorPosicao-TimeMania/
├── app.py                      # Aplicação Flask principal
├── config.py                   # Configurações e constantes
├── requirements.txt            # Dependências Python
├── .env.example               # Exemplo de variáveis de ambiente
├── .gitignore                 # Arquivos ignorados pelo Git
├── README.md                  # Documentação completa
├── QUICKSTART.md              # Guia rápido de início
├── DOWNLOAD.md                # Guia de download de dados
├── ONDE-ESTAO-ARQUIVOS.md     # Mapa de arquivos do projeto
├── database.db                # Banco de dados SQLite (criado automaticamente)
├── models/
│   ├── __init__.py
│   └── resultado_model.py     # Model para resultados da Timemania
├── services/
│   ├── __init__.py
│   ├── api_caixa_service.py   # Integração com API da Caixa
│   ├── estatistica_service.py # Cálculos estatísticos
│   └── timemania_service.py   # Lógica de palpites
├── routes/
│   ├── __init__.py
│   ├── main_routes.py         # Rotas de páginas HTML
│   └── api_routes.py          # Rotas da API REST
├── static/
│   ├── css/
│   │   └── styles.css         # Estilos (cores da Timemania)
│   └── js/
│       └── scripts.js         # JavaScript interativo
└── templates/
    ├── base.html              # Template base
    ├── index.html             # Página principal
    └── palpites.html          # Página de palpites
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+, Flask 3.0
- **Banco de Dados**: SQLite
- **API**: REST com JSON
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Integração**: API oficial da Caixa Econômica Federal

## 📊 Análise Posicional

Uma das características únicas deste sistema é a **análise posicional**, que examina a frequência de cada número em cada uma das 7 posições do sorteio. Isso permite identificar padrões como:
- Números que aparecem mais na 1ª posição (geralmente menores)
- Números que aparecem mais na 7ª posição (geralmente maiores)
- Padrões de distribuição ao longo das posições

## 🏅 Times do Coração

O sistema também oferece análises completas dos Times do Coração:
- **Frequência**: Quantas vezes cada time foi sorteado
- **Times mais sorteados**: Top 10 times com maior frequência
- **Times mais atrasados**: Times que não são sorteados há mais tempo
- **Sugestão inteligente**: Baseada na estratégia escolhida

## ⚠️ Avisos Importantes

1. **Não garantia de premiação**: Este sistema é uma ferramenta de análise estatística. Os palpites são baseados em dados históricos e probabilidades matemáticas, mas não garantem premiação.

2. **Jogo responsável**: Jogue apenas com valores que você pode perder. Loteria deve ser uma diversão, não uma fonte de renda.

3. **Dados oficiais**: Todos os dados são obtidos da API oficial da Caixa Econômica Federal.

4. **Atualização**: Mantenha a base de dados atualizada para ter estatísticas precisas.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Enviar pull requests

## 📝 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

## 🔗 Links Úteis

- [Timemania - Caixa](http://www.caixa.gov.br/loterias/timemania)
- [API da Caixa](https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania)

## 📧 Suporte

Para dúvidas ou suporte, abra uma issue no repositório do GitHub.

---

**Desenvolvido com 💛 e 💚 - As cores da TIMEMANIA**
