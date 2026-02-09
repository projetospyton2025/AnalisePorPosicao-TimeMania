# Guia Rápido - Sistema de Análise TIMEMANIA

Este guia mostra como iniciar o sistema em poucos minutos.

## 🚀 Início Rápido

### 1. Instalar Dependências (1 minuto)

```bash
# Clone o repositório
git clone https://github.com/projetospyton2025/AnalisePorPosicao-TimeMania.git
cd AnalisePorPosicao-TimeMania

# Instale as dependências
pip install -r requirements.txt
```

### 2. Iniciar o Servidor (30 segundos)

```bash
# Inicie a aplicação
python app.py
```

Aguarde a mensagem:
```
Servidor rodando em:
http://0.0.0.0:5058
```

### 3. Acessar no Navegador

Abra seu navegador e acesse:
```
http://localhost:5058
```

### 4. Atualizar Base de Dados (2-3 minutos)

Na primeira vez que usar:
1. Clique em **"Atualizar Dados"** no menu
2. Aguarde o download dos resultados históricos
3. Pronto! O sistema está configurado

## 💡 Próximos Passos

### Visualizar Estatísticas
- Vá para a **página inicial**
- Veja o último resultado
- Explore as estatísticas dos números e times

### Gerar Palpites
1. Clique em **"Gerar Palpites"** no menu
2. Escolha uma estratégia (recomendamos "Equilibrada" para começar)
3. Defina quantos números quer (10 é o mais comum)
4. Clique em **"Gerar Palpites"**
5. O sistema mostra os números e sugere um Time do Coração

### Conferir Palpite
1. Na página de palpites, role até "Conferir Palpite"
2. Digite seus números (separados por vírgula)
3. Digite o Time do Coração
4. Digite o número do concurso
5. Clique em **"Conferir"**

## 🎯 Comandos Úteis

### Via Navegador
```
http://localhost:5058              # Página inicial
http://localhost:5058/palpites     # Gerar palpites
```

### Via API (curl)
```bash
# Atualizar base
curl -X POST http://localhost:5058/api/atualizar

# Ver último resultado
curl http://localhost:5058/api/ultimo-resultado

# Ver estatísticas
curl http://localhost:5058/api/estatisticas

# Gerar palpite
curl -X POST http://localhost:5058/api/gerar-palpite \
  -H "Content-Type: application/json" \
  -d '{"estrategia": "equilibrada", "quantidade_numeros": 10, "quantidade_jogos": 1}'
```

## 🔧 Configurações Opcionais

### Porta Personalizada
Edite o arquivo `.env`:
```bash
PORT=8080  # Altere para a porta desejada
```

### Modo Debug
```bash
DEBUG=True   # Para desenvolvimento
DEBUG=False  # Para produção
```

## ❓ Problemas Comuns

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
Altere a porta no arquivo `.env` ou:
```bash
PORT=5059 python app.py
```

### "Database locked"
Feche outras instâncias do sistema e tente novamente.

## 📊 Estratégias Recomendadas

- **Primeira vez?** Use **Equilibrada**
- **Quer arriscar?** Use **Agressiva**
- **Quer jogar seguro?** Use **Conservadora**
- **Quer diversificar?** Use **Mista**
- **Acredita em ciclos?** Use **Atrasados**

## 🎲 Dica de Ouro

💡 **Combine estratégias**: Gere vários jogos com diferentes estratégias para aumentar suas chances de cobertura!

Exemplo:
- 2 jogos com estratégia "Equilibrada"
- 2 jogos com estratégia "Por Posição"
- 1 jogo com estratégia "Atrasados"

## 📖 Precisa de Mais Ajuda?

Consulte a documentação completa no arquivo `README.md`

---

**Boa sorte! 🍀**
