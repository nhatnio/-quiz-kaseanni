# quiz_kaseanni.py – Quiz mit Multi-Choice Fix (SessionState-Fehler korrigiert)
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

    if qtype == "Checkbox" or qtype == "MCQ-Multi":
        # Nur anzeigen, nicht manuell schreiben in session_state
        default_val = st.session_state.user_answers.get(key, [])
        user_input = st.multiselect("Wählen Sie eine oder mehrere Antworten:", options, default=default_val, key=key)
    elif qtype == "MCQ":
        default_val = st.session_state.user_answers.get(key, options[0])
        user_input = st.radio("Wählen Sie eine Antwort:", options, index=options.index(default_val), key=key)
    elif qtype == "Matching":
        default_val = st.session_state.user_answers.get(key, "")
        user_input = st.text_input("Ihre Zuordnung:", value=default_val, key=key)
    elif qtype == "Sequence":
        default_val = st.session_state.user_answers.get(key, "")
        user_input = st.text_input("Reihenfolge:", value=default_val, key=key)
    else:
        st.warning("❗ Unbekannter Fragetyp")
        user_input = None

    # Speichere nur beim Weiter/Zürück
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Zurück") and st.session_state.current_question > 0:
            st.session_state.user_answers[key] = user_input
            st.session_state.current_question -= 1
    with col2:
        if st.button("➡️ Weiter") and st.session_state.current_question < total_questions - 1:
            st.session_state.user_answers[key] = user_input
            st.session_state.current_question += 1

    st.markdown("---")
    if st.button("✅ Quiz abgeben"):
        st.session_state.user_answers[key] = user_input
        st.session_state.submitted = True

    if st.session_state.submitted:
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
