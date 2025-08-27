# app/llm_mock.py
from typing import List, Dict


def generate_mock_questions(text: str, n: int = 3) -> List[Dict]:
    """
    Deterministic-ish mock generator (placeholders).
    Honra o parâmetro n e usa chaves esperadas pelo app.
    """
    items: List[Dict] = []
    for i in range(n):
        items.append({
            "question": f"question{i+1}",
            "answer_index": 0,  # índice da alternativa correta
            "options": ["opt1", "opt2", "opt3", "opt4"],
            "rationale": "mock rationale: resposta correta é a primeira opção neste placeholder."
        })
    return items
