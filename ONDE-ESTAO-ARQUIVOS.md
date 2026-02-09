# Onde Estão os Arquivos - TIMEMANIA

Mapa completo da estrutura de arquivos e suas responsabilidades.

## 📂 Estrutura Geral

```
AnalisePorPosicao-TimeMania/
├── 📄 Arquivos de Configuração
├── 📁 models/          (Banco de Dados)
├── 📁 services/        (Lógica de Negócio)
├── 📁 routes/          (Endpoints e Páginas)
├── 📁 static/          (Frontend - CSS/JS)
├── 📁 templates/       (Frontend - HTML)
└── 📄 Documentação
```

---

## 📄 Arquivos de Configuração

### `app.py`
**Localização:** `/app.py`  
**Propósito:** Aplicação Flask principal  
**Responsabilidades:**
- Inicializa o servidor Flask
- Registra os blueprints (rotas)
- Define configurações do servidor
- Roda na porta 5058

**Quando modificar:**
- Adicionar novos blueprints
- Alterar configurações globais
- Adicionar middleware

### `config.py`
**Localização:** `/config.py`  
**Propósito:** Configurações e constantes do sistema  
**Responsabilidades:**
- Define porta do servidor (5058)
- URLs da API da Caixa
- Constantes da Timemania (MIN/MAX números, etc.)
- Cores da identidade visual
- Estratégias disponíveis

**Quando modificar:**
- Alterar configurações globais
- Adicionar novas constantes
- Modificar paletas de cores

### `requirements.txt`
**Localização:** `/requirements.txt`  
**Propósito:** Dependências Python  
**Conteúdo:**
- Flask 3.0.0
- requests 2.31.0
- python-dotenv 1.0.0

**Quando modificar:**
- Adicionar novas bibliotecas
- Atualizar versões

### `.env.example`
**Localização:** `/.env.example`  
**Propósito:** Exemplo de variáveis de ambiente  
**Conteúdo:**
- SECRET_KEY
- DEBUG
- HOST/PORT
- DATABASE_PATH
- API_TIMEMANIA_URL

**Como usar:**
```bash
cp .env.example .env
# Edite .env conforme necessário
```

### `.gitignore`
**Localização:** `/.gitignore`  
**Propósito:** Arquivos ignorados pelo Git  
**Ignora:**
- `__pycache__/`
- `.env`
- `database.db`
- Arquivos temporários

---

## 📁 models/ - Banco de Dados

### `models/__init__.py`
**Localização:** `/models/__init__.py`  
**Propósito:** Inicialização do módulo  
**Exporta:** `ResultadoModel`

### `models/resultado_model.py`
**Localização:** `/models/resultado_model.py`  
**Propósito:** Model para resultados da Timemania  
**Responsabilidades:**
- Criar tabela SQLite
- Inserir/atualizar resultados
- Buscar resultados (último, todos, por número)
- Gerenciar banco de dados

**Métodos principais:**
- `inserir(resultado)` - Salva resultado
- `buscar_ultimo()` - Último concurso
- `buscar_todos(limite)` - Lista concursos
- `buscar_por_numero(numero)` - Concurso específico
- `contar_resultados()` - Total de concursos

**Quando modificar:**
- Adicionar novos campos na tabela
- Criar novos métodos de consulta
- Otimizar queries

---

## 📁 services/ - Lógica de Negócio

### `services/__init__.py`
**Localização:** `/services/__init__.py`  
**Propósito:** Inicialização do módulo  
**Exporta:** `ApiCaixaService`, `EstatisticaService`, `TimemaniaService`

### `services/api_caixa_service.py`
**Localização:** `/services/api_caixa_service.py`  
**Propósito:** Integração com API da Caixa  
**Responsabilidades:**
- Buscar último concurso
- Buscar concurso específico
- Atualizar base completa
- Tratar erros de API

**Métodos principais:**
- `buscar_ultimo_concurso()` - GET último resultado
- `buscar_concurso_especifico(numero)` - GET por número
- `atualizar_base_completa()` - Atualização incremental

**Quando modificar:**
- API da Caixa mudar
- Adicionar novos endpoints
- Melhorar tratamento de erros

### `services/estatistica_service.py`
**Localização:** `/services/estatistica_service.py`  
**Propósito:** Cálculos estatísticos  
**Responsabilidades:**
- Calcular frequência de números
- Calcular atrasos
- Análise pares/ímpares
- Análise por faixa
- Análise por dígito
- **Análise por posição de sorteio**
- Estatísticas dos Times do Coração

**Métodos principais:**
- `calcular_estatisticas_completas()` - Todas estatísticas
- `calcular_frequencia_numeros()` - Frequência 01-80
- `calcular_atrasos()` - Números atrasados
- `calcular_pares_impares()` - Distribuição
- `calcular_por_faixa()` - Por faixas de dezenas
- `calcular_por_digito()` - Por dígito final
- `calcular_por_posicao_sorteio()` - **Análise posicional**
- `calcular_frequencia_times_coracao()` - Times
- `calcular_times_mais_sorteados()` - Top times
- `calcular_times_mais_atrasados()` - Times atrasados

**Quando modificar:**
- Adicionar novas análises estatísticas
- Otimizar cálculos
- Adicionar cache

### `services/timemania_service.py`
**Localização:** `/services/timemania_service.py`  
**Propósito:** Geração de palpites  
**Responsabilidades:**
- Gerar palpites por estratégia
- Sugerir Time do Coração
- Conferir palpites

**Estratégias implementadas:**
1. Equilibrada
2. Agressiva
3. Conservadora
4. Mista
5. Atrasados
6. Por Faixa
7. Por Posição

**Métodos principais:**
- `gerar_palpite(estrategia, qtd_numeros, qtd_jogos)` - Gera jogos
- `sugerir_time_coracao(estrategia)` - Sugere time
- `conferir_palpite(numeros, time, concurso)` - Confere aposta

**Quando modificar:**
- Adicionar novas estratégias
- Melhorar algoritmos existentes
- Ajustar pesos e probabilidades

---

## 📁 routes/ - Endpoints e Páginas

### `routes/__init__.py`
**Localização:** `/routes/__init__.py`  
**Propósito:** Inicialização do módulo  
**Exporta:** `main_bp`, `api_bp`

### `routes/main_routes.py`
**Localização:** `/routes/main_routes.py`  
**Propósito:** Rotas de páginas HTML  
**Rotas:**
- `GET /` - Página inicial
- `GET /palpites` - Página de palpites

**Quando modificar:**
- Adicionar novas páginas
- Modificar URLs

### `routes/api_routes.py`
**Localização:** `/routes/api_routes.py`  
**Propósito:** API REST  
**Rotas:**
- `POST /api/atualizar` - Atualiza base
- `GET /api/ultimo-resultado` - Último concurso
- `GET /api/resultados` - Lista concursos
- `GET /api/resultado/<numero>` - Concurso específico
- `GET /api/estatisticas` - Todas estatísticas
- `GET /api/estatisticas/times-coracao` - Stats times
- `GET /api/sugerir-time-coracao` - Sugere time
- `POST /api/gerar-palpite` - Gera palpites
- `POST /api/conferir` - Confere aposta
- `GET /api/health` - Health check

**Quando modificar:**
- Adicionar novos endpoints
- Modificar validações
- Adicionar autenticação

---

## 📁 static/ - Frontend (CSS/JS)

### `static/css/styles.css`
**Localização:** `/static/css/styles.css`  
**Propósito:** Estilos do sistema  
**Características:**
- Cores da Timemania (Amarelo #FFF600, Verde #12923D)
- Design responsivo
- Gradientes amarelo-verde
- Cards, tabelas, formulários
- Animações e transições

**Seções:**
- Reset e configurações gerais
- Header e navegação
- Cards e grids
- Números e Time do Coração
- Formulários e botões
- Tabelas
- Responsividade
- Utilitários

**Quando modificar:**
- Alterar cores ou estilos
- Adicionar novos componentes
- Melhorar responsividade

### `static/js/scripts.js`
**Localização:** `/static/js/scripts.js`  
**Propósito:** JavaScript do sistema  
**Responsabilidades:**
- Chamadas à API
- Atualização dinâmica
- Geração de palpites
- Conferência de apostas
- Formatação de dados

**Funções principais:**
- `atualizarBase()` - Atualiza dados
- `carregarUltimoResultado()` - Carrega último
- `carregarEstatisticas()` - Carrega stats
- `gerarPalpites()` - Gera jogos
- `conferirPalpite()` - Confere aposta

**Quando modificar:**
- Adicionar interatividade
- Melhorar UX
- Adicionar gráficos

---

## 📁 templates/ - Frontend (HTML)

### `templates/base.html`
**Localização:** `/templates/base.html`  
**Propósito:** Template base  
**Conteúdo:**
- Header com logo
- Navegação
- Bloco de conteúdo
- Footer
- Links CSS/JS

**Quando modificar:**
- Alterar estrutura geral
- Modificar header/footer
- Adicionar meta tags

### `templates/index.html`
**Localização:** `/templates/index.html`  
**Propósito:** Página principal  
**Conteúdo:**
- Último resultado
- Estatísticas gerais
- Informações sobre Timemania
- Estratégias disponíveis

**Quando modificar:**
- Alterar layout da home
- Adicionar seções

### `templates/palpites.html`
**Localização:** `/templates/palpites.html`  
**Propósito:** Página de palpites  
**Conteúdo:**
- Formulário de geração
- Resultado dos palpites
- Conferência de apostas
- Dicas e informações

**Quando modificar:**
- Alterar formulários
- Adicionar funcionalidades

---

## 📄 Documentação

### `README.md`
**Propósito:** Documentação completa  
**Conteúdo:**
- Sobre o sistema
- Instalação
- Como usar
- API REST
- Estrutura
- Tecnologias

### `QUICKSTART.md`
**Propósito:** Guia rápido de início  
**Conteúdo:**
- Início em minutos
- Comandos essenciais
- Problemas comuns

### `DOWNLOAD.md`
**Propósito:** Guia de download de dados  
**Conteúdo:**
- Download inicial
- Atualizações
- Fonte dos dados
- Troubleshooting

### `ONDE-ESTAO-ARQUIVOS.md`
**Propósito:** Este arquivo  
**Conteúdo:**
- Mapa de arquivos
- Responsabilidades
- Quando modificar

---

## 🗄️ Banco de Dados

### `database.db`
**Localização:** `/database.db` (criado automaticamente)  
**Propósito:** Armazenar resultados  
**Tipo:** SQLite  
**Tabelas:**
- `resultados` - Todos os concursos

**Quando modificar:**
- Nunca edite manualmente
- Use os métodos do Model
- Faça backups antes de migrações

---

## 🔍 Como Encontrar o Que Procura

### Precisa modificar...

**...a porta do servidor?**
→ `config.py` ou `.env`

**...as cores da interface?**
→ `static/css/styles.css`

**...adicionar nova estratégia?**
→ `services/timemania_service.py`

**...adicionar nova estatística?**
→ `services/estatistica_service.py`

**...adicionar novo endpoint?**
→ `routes/api_routes.py`

**...modificar o layout?**
→ `templates/*.html`

**...adicionar interatividade?**
→ `static/js/scripts.js`

**...consultar o banco?**
→ `models/resultado_model.py`

**...integrar nova API?**
→ `services/api_caixa_service.py`

---

## 📊 Fluxo de Dados

```
API Caixa → api_caixa_service.py → resultado_model.py → database.db
                                                           ↓
database.db → resultado_model.py → estatistica_service.py → API REST
                                                           ↓
API REST → scripts.js → templates/*.html → Navegador
```

---

**Dica:** Use a busca do seu editor (Ctrl+F ou Cmd+F) para encontrar rapidamente funções ou classes específicas!
