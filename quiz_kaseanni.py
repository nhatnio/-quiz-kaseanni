# quiz_kaseanni.py – Optimiert: Navigation sofort & Multi-Choice durch Textantwort ersetzt
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
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'navigate' not in st.session_state:
    st.session_state.navigate = None

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
    default_val = st.session_state.user_answers.get(key, "")

    if qtype in ["Checkbox", "MCQ-Multi"]:
        user_input = st.text_input("Geben Sie Ihre gewählten Buchstaben durch Kommas getrennt ein (z. B.: A, C, D):", value=default_val, key=key)
    elif qtype == "MCQ":
        user_input = st.radio("Wählen Sie eine Antwort:", options, index=options.index(default_val) if default_val in options else 0, key=key)
    elif qtype == "Matching":
        user_input = st.text_input("Ihre Zuordnung:", value=default_val, key=key)
    elif qtype == "Sequence":
        user_input = st.text_input("Reihenfolge:", value=default_val, key=key)
    else:
        st.warning("❗ Unbekannter Fragetyp")
        user_input = ""

    st.session_state.user_answers[key] = user_input

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Zurück") and st.session_state.current_question > 0:
            st.session_state.navigate = "back"
    with col2:
        if st.button("➡️ Weiter") and st.session_state.current_question < total_questions - 1:
            st.session_state.navigate = "next"

    if st.session_state.navigate == "back":
        st.session_state.current_question -= 1
        st.experimental_rerun()
    elif st.session_state.navigate == "next":
        st.session_state.current_question += 1
        st.experimental_rerun()

    st.markdown("---")
    if st.button("✅ Quiz abgeben"):
        st.session_state.submitted = True

    if st.session_state.submitted:
        st.markdown("## ✅ Auswertung")
        score = 0
        for i in range(total_questions):
            row = df.iloc[i]
            correct = row['Correct Answer(s)']
            given = st.session_state.user_answers.get(f"q_{i}", "")
            correct_str = str(correct).strip().lower()
            given_str = ', '.join(sorted(g.strip() for g in given.split(","))).lower() if ("," in given) else str(given).strip().lower()
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
