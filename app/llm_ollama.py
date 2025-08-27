import json
import os
import re
from typing import Dict, List, Any
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b-instruct")


def _build_prompt(text: str, n: int) -> str:
    prompt=f"""
        Contexto:  Você é um gerador especializado em **perguntas de múltipla escolha** para fins   
        educacionais. Você vai receber o conteúdo de uma aula. Esse conteúdo é apenas 
        a base de conhecimento.

        Tarefa: A partir do conteúdo fornecido a seguir, você deve criar uma única pergunta objetiva 
        de múltipla escolha que avalie a compreensão de um ponto importante do texto.

        texto = '''{text}'''


        Ação: Produza a saída estritamente no formato JSON a seguir, sem incluir explicações adicionais, 
        sem markdown e sem comentários:
        {
        '  question: enunciado claro e curto,'
        '  options: [alternativa A, alternativa B, alternativa C, alternativa D],'
        '  answer_index: número_da_correta (0 a 3),'
        '  rationale: breve justificativa da alternativa correta'
        }

        Regras adicionais:
        - A pergunta não deve ser copiada literalmente do texto, mas baseada nele.
        - Use linguagem clara, com até 25 palavras no enunciado.
        - Sempre 4 alternativas plausíveis, sendo apenas 1 correta.
        - O índice da correta deve corresponder exatamente à posição no array 'options'.
        - A justificativa deve ter no máximo 2 frases.
        - Gere **somente um objeto JSON**, nada mais.

    """
    return prompt



def _extract_json(s: str) -> Any:
    """
    Tenta carregar JSON diretamente; caso venha texto ao redor, tenta extrair o primeiro bloco JSON.
    """
    # tentativa direta
    try:
        return json.loads(s)
    except Exception:
        pass

    # tenta capturar o maior objeto JSON ({...}) ou array ([...])
    match = re.search(r"(\{.*\}|\[.*\])", s, flags=re.DOTALL)
    if match:
        snippet = match.group(1)
        return json.loads(snippet)
    raise ValueError("Resposta não contém JSON válido.")


def _post_ollama_generate(prompt: str, model: str, host: str) -> str:
    url = f"{host.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 2048,
            "num_predict": 256,
            "repeat_penalty": 1.05
        }
    }
    resp = requests.post(url, json=payload, timeout=600)
    resp.raise_for_status()
    data = resp.json()
    print('!!!!!!!!')
    print(data)
    print('!!!!!!!!')
    # /api/generate retorna {"response": "..."} quando stream=False
    return data.get("response", "")


def generate_questions_via_ollama(text: str, n: int = 3,
                                  model: str | None = None,
                                  host: str | None = None) -> List[Dict]:
    model = model or OLLAMA_MODEL
    host = host or OLLAMA_HOST
    prompt = _build_prompt(text, n)
    raw = _post_ollama_generate(prompt, model, host)
    print(raw)
    parsed = _extract_json(raw)
    print(parsed)
    return [parsed]
