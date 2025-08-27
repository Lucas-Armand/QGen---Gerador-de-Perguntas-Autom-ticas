import json
from datetime import datetime
import streamlit as st
from llm_mock import generate_mock_questions

st.set_page_config(page_title="QGen — MVP", layout="wide")

# Estado mínimo
if "text" not in st.session_state:
    st.session_state.text = ""
if "questions" not in st.session_state:
    st.session_state.questions = []
if "n_questions" not in st.session_state:
    st.session_state.n_questions = 3

# Navegação
pages = ["Upload", "Results"]
selected = st.sidebar.radio("Navigation", pages)

# ---------------------------
# Página: Upload
# ---------------------------
if selected == "Upload":
    st.title("QGen — Upload")
    st.caption("Envie um .txt ou cole o conteúdo da aula")

    uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])
    st.write("ou")
    manual = st.text_area("Paste the lesson text here", height=200, placeholder="Cole o texto da aula...")

    n_q = st.number_input("Number of questions", 1, 20, st.session_state.n_questions, 1)

    col1, col2 = st.columns([1, 1])
    with col1:
        generate_btn = st.button("Generate (Mock)", type="primary")
    with col2:
        clear_btn = st.button("Clear")

    if clear_btn:
        st.session_state.text = ""
        st.session_state.questions = []
        st.session_state.n_questions = 3
        st.success("Cleared.")

    if generate_btn:
        text = ""
        if uploaded_file is not None:
            try:
                text = uploaded_file.read().decode("utf-8", errors="ignore")
            except Exception:
                st.error("Could not read file. Check encoding (UTF-8).")
        elif manual.strip():
            text = manual.strip()

        if not text:
            st.info("Please upload a .txt file or paste some text.")
        else:
            st.session_state.text = text
            st.session_state.n_questions = int(n_q)
            qs = generate_mock_questions(text, n=int(n_q))
            if not qs:
                st.warning("No questions generated (text too short?). Try with a longer content.")
            else:
                st.session_state.questions = qs
                st.success(f"Generated {len(qs)} questions. Go to **Results** in the sidebar.")

    # Preview simples do texto
    if st.session_state.text:
        st.subheader("Preview (first 1500 chars)")
        st.text(st.session_state.text[:1500])

# ---------------------------
# Página: Results
# ---------------------------
elif selected == "Results":
    st.title("QGen — Results")

    qs = st.session_state.get("questions", [])
    if not qs:
        st.info("No questions available. Go to **Upload** and generate first.")
    else:
        # Render compacto: cada pergunta em um container
        for i, q in enumerate(qs, start=1):
            with st.container(border=True):
                st.markdown(f"**Question {i}**")
                st.write(q.get("question", ""))

                # Alternativas (somente listagem)
                opts = q.get("options", [])
                answer_idx = q.get("answer_idx", 0)

                # Exibição simples: tabela de alternativas
                st.write("Options:")
                for idx, opt in enumerate(opts):
                    prefix = "✅ " if idx == answer_idx else "• "
                    st.write(f"{prefix}{opt}")

                with st.expander("Rationale"):
                    st.write(q.get("rationale", ""))

        # Pacote de export
        export = {
            "meta": {
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "backend": "mock",
                "count": len(qs)
            },
            "items": qs
        }

        st.divider()
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(export, ensure_ascii=False, indent=2),
            file_name="qgen_mock_questions.json",
            mime="application/json"
        )

        st.caption("Tip: regenerar no menu **Upload** mantém o fluxo simples e limpo.")

