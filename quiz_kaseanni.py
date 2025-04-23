# quiz_kaseanni.py – Version mit einer Frage pro Seite (mit Antwortspeicherung)
import streamlit as st
st.set_page_config(page_title="🧀 Quiz: Kaseanni – Käsekunde", layout="wide")

import pandas as pd

@st.cache_data
def load_data():
    try:
        return pd.read_excel("quiz_data_kaseanni.xlsx")
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Excel-Datei: {e}")
        return None

# Initialisiere Session State
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'score' not in st.session_state:
    st.session_state.score = 0

# Daten laden
df = load_data()

st.title("🧀 Quiz: Kaseanni – Fachwissen zu Käse und Wein")

if df is not None:
    total_questions = len(df)
    q_index = st.session_state.current_question
    row = df.iloc[q_index]

    st.markdown(f"### Frage {q_index + 1} von {total_questions}")
    st.markdown(row['Question'])

    qtype = row['Type']
    options = [row[f'Option {i}'] for i in range(1, 7) if pd.notna(row.get(f'Option {i}'))]

    key = f"q_{q_index}"
    default_answer = st.session_state.user_answers.get(key, []) if qtype == "Checkbox" else st.session_state.user_answers.get(key, "")

    user_input = None
    if qtype == "MCQ":
        user_input = st.radio("Wählen Sie eine Antwort:", options, index=options.index(default_answer) if default_answer in options else 0, key=key)
    elif qtype == "Checkbox":
        user_input = st.multiselect("Wählen Sie alle richtigen Antworten:", options, default=default_answer, key=key)
    elif qtype == "Matching":
        st.info("Bitte geben Sie die passende Zuordnung ein (z. B.: A → 1, B → 2…)")
        user_input = st.text_input("Ihre Zuordnung:", value=default_answer, key=key)
    elif qtype == "Sequence":
        st.info("Bitte geben Sie die richtige Reihenfolge ein, z. B.: 1–2–3–4")
        user_input = st.text_input("Reihenfolge:", value=default_answer, key=key)
    else:
        st.warning("❗ Unbekannter Fragetyp")

    if st.button("👉 Weiter"):
        st.session_state.user_answers[key] = user_input
        st.session_state.current_question += 1

    if st.session_state.current_question >= total_questions:
        st.markdown("## ✅ Auswertung")
        score = 0
        for i in range(total_questions):
            row = df.iloc[i]
            correct = row['Correct Answer(s)']
            given = st.session_state.user_answers.get(f"q_{i}", "")
            correct_str = str(correct).strip().lower()
            given_str = ', '.join(sorted(given)).lower() if isinstance(given, list) else str(given).strip().lower()
            st.markdown(f"### Frage {i + 1}:")
            if correct_str == given_str:
                st.success("✔️ Richtig")
                score += 1
            else:
                st.error(f"❌ Falsch – Richtige Antwort: {correct}")

        st.success(f"### 🧾 Gesamtpunktzahl: {score} von {total_questions}")
        st.stop()
else:
    st.stop()
