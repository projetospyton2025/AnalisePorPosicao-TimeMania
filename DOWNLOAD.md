# Guia de Download de Dados - TIMEMANIA

Este guia explica como baixar e atualizar os dados históricos da TIMEMANIA.

## 📥 Download Inicial

### Método 1: Via Interface Web (Recomendado)

1. **Inicie o servidor:**
```bash
python app.py
```

2. **Acesse no navegador:**
```
http://localhost:5058
```

3. **Clique em "Atualizar Dados"** no menu superior

4. **Aguarde o download:**
   - O sistema busca automaticamente os últimos 100 concursos
   - Pode levar 2-3 minutos dependendo da conexão
   - Uma mensagem confirmará o sucesso

### Método 2: Via API (Terminal)

```bash
curl -X POST http://localhost:5058/api/atualizar
```

Resposta esperada:
```json
{
  "sucesso": true,
  "mensagem": "Base atualizada com sucesso",
  "total_cadastrados": 100,
  "novos": 100,
  "erros": 0,
  "ultimo_concurso": 2277
}
```

### Método 3: Via Python Script

Crie um arquivo `download_dados.py`:

```python
import requests

API_URL = "http://localhost:5058/api/atualizar"

print("Iniciando download dos dados...")
response = requests.post(API_URL)
data = response.json()

if data.get('sucesso'):
    print(f"✓ Download concluído!")
    print(f"  - Total cadastrados: {data.get('total_cadastrados')}")
    print(f"  - Novos concursos: {data.get('novos')}")
    print(f"  - Último concurso: {data.get('ultimo_concurso')}")
else:
    print(f"✗ Erro: {data.get('mensagem')}")
```

Execute:
```bash
python download_dados.py
```

## 🔄 Atualizações Periódicas

### Frequência Recomendada

A TIMEMANIA tem sorteios regulares. Recomendamos atualizar:
- **Após cada sorteio** (geralmente 3x por semana)
- **Semanalmente** para garantir dados atualizados
- **Antes de gerar palpites** para estatísticas precisas

### Atualização Automática

O sistema detecta automaticamente se há novos concursos e busca apenas os que faltam.

**Exemplo:**
- Base atual: concursos 1 a 2270
- API da Caixa: concursos até 2277
- Sistema baixa: apenas concursos 2271 a 2277

### Verificar Status da Base

Via API:
```bash
curl http://localhost:5058/api/health
```

Resposta:
```json
{
  "sucesso": true,
  "status": "online",
  "total_concursos": 100,
  "ultimo_concurso": 2277
}
```

## 📊 Fonte dos Dados

### API Oficial da Caixa

**URL Base:**
```
https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania
```

**Endpoints:**
- Último concurso: `GET /timemania`
- Concurso específico: `GET /timemania/{numero}`

### Estrutura dos Dados

Cada concurso inclui:
- ✅ Número do concurso
- ✅ Data do sorteio
- ✅ 7 números sorteados (ordem e ordenados)
- ✅ Time do Coração
- ✅ Informações de premiação
- ✅ Valores arrecadados
- ✅ Próximo concurso

## 🗄️ Banco de Dados

### Localização

O banco de dados SQLite é criado automaticamente em:
```
AnalisePorPosicao-TimeMania/database.db
```

### Estrutura

Tabela `resultados`:
- Campos completos da API
- Time do Coração (nome e número)
- Números em ordem de sorteio e ordenados
- Informações de premiação

### Backup Manual

```bash
# Backup
cp database.db database_backup_$(date +%Y%m%d).db

# Restaurar
cp database_backup_20250209.db database.db
```

## 🔍 Verificar Dados

### Via Python

```python
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Contar concursos
cursor.execute('SELECT COUNT(*) FROM resultados')
print(f"Total de concursos: {cursor.fetchone()[0]}")

# Último concurso
cursor.execute('SELECT numero, dataApuracao FROM resultados ORDER BY numero DESC LIMIT 1')
ultimo = cursor.fetchone()
print(f"Último concurso: {ultimo[0]} - {ultimo[1]}")

conn.close()
```

### Via SQL

```bash
sqlite3 database.db "SELECT COUNT(*) FROM resultados;"
sqlite3 database.db "SELECT numero, dataApuracao FROM resultados ORDER BY numero DESC LIMIT 5;"
```

## ⚠️ Resolução de Problemas

### Erro: "API não responde"
- Verifique sua conexão com a internet
- A API da Caixa pode estar temporariamente indisponível
- Tente novamente em alguns minutos

### Erro: "Database locked"
- Feche outras instâncias do sistema
- Aguarde alguns segundos e tente novamente

### Erro: "Nenhum concurso encontrado"
- Faça o download inicial via "Atualizar Dados"
- Verifique se o servidor está rodando

### Download Muito Lento
- A API da Caixa tem limite de requisições
- O sistema busca um concurso por vez para evitar bloqueios
- Seja paciente, especialmente no primeiro download

## 📈 Boas Práticas

1. **Backup Regular**: Faça backup do database.db semanalmente
2. **Atualização Frequente**: Atualize após cada sorteio
3. **Verificação**: Sempre verifique o último concurso cadastrado
4. **Conexão Estável**: Use conexão estável para downloads grandes

## 🔐 Segurança dos Dados

- ✅ Dados armazenados localmente
- ✅ Sem envio de informações pessoais
- ✅ API pública da Caixa (sem autenticação)
- ✅ Banco SQLite criptografável (opcional)

## 📊 Estatísticas do Download

**Tempo médio de download:**
- Primeiro download (100 concursos): 2-3 minutos
- Atualização incremental (1-10 concursos): 10-30 segundos

**Tamanho do banco de dados:**
- 100 concursos: ~500KB
- 1000 concursos: ~5MB
- 2000 concursos: ~10MB

## 📞 Suporte

Problemas com download?
1. Verifique os logs no terminal
2. Consulte a seção de problemas comuns
3. Abra uma issue no GitHub

---

**Dados sempre atualizados = Estatísticas precisas = Melhores palpites!**
