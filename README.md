# QGen — Gerador de Perguntas Automáticas (Start do Projeto)

Plataforma simples (Streamlit + Docker) para **gerar perguntas de múltipla escolha** a partir do conteúdo um texto de aula. 

A app deve rodar em dois modos:
1) **Local** usando modelos abertos (ex.: `llama3.2:3b-instruct`, `mistral:7b-instruct`);
2) **Nuvem** usando algum modelo gratuita (via Google Gemini (AI Studio) ou OpenRouter).


---

## Problema & Objetivo

Educadores e criadores de conteúdo precisam transformar rapidamente **textos de aula** em **itens de avaliação**. O objetivo é entregar um **MVP funcional** que:
- receba um **.txt**,
- gere **perguntas com alternativas** (gabarito + explicação curta),
- solução baseada em LLM,
- permita alternar entre **LLM local** e **LLM online** (chave opcional),

---

## Escopo do MVP (primeira entrega)

- **Tela 1 (Upload)**: usuário sobe um `.txt` com o conteúdo da aula.
- **Tela 2 (Resultados)**: exibe as perguntas geradas com:
  - enunciado,
  - 4 alternativas (1 correta + 3 distratores),
  - “racional”/explicação curta,
  - botão para **exporta pergunta**.

---

## Visão Técnica (curta)

- **Frontend**: Streamlit  
- **LLM**:
  - **Local** (Ollama): `llama3.2:3b-instruct` ou `mistral:7b-instruct`
  - **Online** (opcional): Gemini (AI Studio) ou OpenRouter
- **Empacotamento**: Docker (um container para a app; Ollama pode ser externo ou um 2º container)

### Fluxo (MVP)

[Upload .txt] → [Pré-processamento leve] → [Gerador (LLM local/online ou baseline)] → [Render na UI] → [Export]

## Roadmap (Baby Steps)

**ETAPA 1 —  Início**
- [x] Estrutura do app (Streamlit + rotas entre telas)
- [x] Upload `.txt` e armazenamento temporário
- [x] LLM Mockado
- [x] Tela de resultados 
- [ ] Ler papers sobre Geração de Perguntas com LLM

**ETAPA 2 — LLM Local**
- [ ] Client Ollama (HTTP) com modelo configurável
- [ ] Prompt base 

**ETAPA 3 — LLM Online (opcional)**
- [ ] Integração Gemini (AI Studio)

**ETAPA 4 — Qualidade & DX**
- [ ] Heurísticas: filtrar sentenças curtas/repetidas; evitar termos triviais
- [ ] Métricas simples sobre a qualidade das perguntas e respostas
- [ ] Testes mínimos 
- [ ] Dockerfile + docker-compose (app e, opcionalmente, serviço llm)

**ETAPA 5 — Próximos Passos (não-MVP)**
- [ ] Planejar próximos passos
---

## Estrutura Inicial (proposta)

```
./
├── app
│   ├── app.py
│   ├── llm_mock.py
│   └── __pycache__
│       └── llm_mock.cpython-38.pyc
├── README.md
├── requirements.txt
└── sample
    └── aula.txt
```

---

## Riscos & Mitigações

- **Limites de API Free**: manter fallback local e baseline.
- **Qualidade dos distratores**: começar simples (vocabulário do texto) e evoluir com LLM local.
- **Tempo de inferência**: preferir prompts curtos, modelos leves; streaming opcional.
- **Variabilidade do LLM**: padronizar instruções e pós-processar para formato JSON estrito.

---

## Diário — 2025-08-26 (esboço & planejamento)

- **Decisões do dia**:
  - Escopo do MVP com **2 telas** (Upload → Resultados).
  - Suporte a **4 backends**: `baseline`, `ollama`, `gemini`, `openrouter`.
  - Saída única em **JSON** para facilitar testes e integração.
- **Tarefas mapeadas**:
  - Criar estrutura de pastas e arquivos base.
  - Implementar baseline **sem LLM** (TF-IDF + cloze + distratores do próprio texto).
  - Definir prompt inicial (português, objetivo, 1 correta + 3 distratores + racional).
  - Especificar `.env` e selector de backend no Streamlit.
  - Esboçar Dockerfile e docker-compose (app + opcional llm).
- **Pendências**:
  - Escolha final dos modelos (começar com `mistral:7b-instruct` no Ollama).
  - Teste rápido de latência/saída (comparar baseline vs. LLM local).
  - Ajustar fallback de forma transparente (mensagem na UI).
- **Papers para ler amanhã** (selecionados hoje na pesquisa):
  1) Li, K., & Zhang, Y. (2024). *Planning First, Question Second: An LLM-Guided Method for Controllable Question Generation* (ACL Findings 2024).
  2) Mucciaccia, S. S., et al. (2025). *Automatic Multiple-Choice Question Generation and Evaluation Systems Based on LLM* (COLING 2025).
  3) Tan, B., et al. (2025). *A Review of Automatic Item Generation Techniques Leveraging Large Language Models* (IJATE 2025).

---

## Como rodar (rascunho)

**Local (sem Docker, com baseline):**
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # ajustar LLM_BACKEND=baseline
streamlit run app/app.py
```

**Local + Ollama:**
```
ollama pull mistral:7b-instruct
# .env → LLM_BACKEND=ollama | OLLAMA_HOST=http://localhost:11434 | OLLAMA_MODEL=mistral:7b-instruct
streamlit run app/app.py
```

**Docker (rascunho):**
```
docker-compose up --build
# app em http://localhost:8501
```

---

## Licença
A definir (provável MIT).
