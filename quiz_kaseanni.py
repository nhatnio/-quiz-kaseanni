# quiz_kaseanni.py – Streamlit Quiz App für Käsekunde "Kaseanni"
import streamlit as st
import pandas as pd

# Excel-Datei laden mit Fehlerbehandlung
@st.cache_data
def load_data():
    try:
        return pd.read_excel("quiz_data_kaseanni.xlsx")
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der Excel-Datei: {e}")
        return None

# Daten laden
df = load_data()

st.set_page_config(page_title="🧀 Quiz: Kaseanni – Käsekunde", layout="wide")
st.title("🧀 Quiz: Kaseanni – Fachwissen zu Käse und Wein")

if df is not None:
    score = 0
    user_answers = []
    df = df.sample(frac=1).reset_index(drop=True)  # Fragen mischen

    def render_question(row, index):
        st.markdown(f"### {index + 1}. {row['Question']}")
        qtype = row['Type']
        options = [row[f'Option {i}'] for i in range(1, 7) if pd.notna(row.get(f'Option {i}'))]

        if qtype == "MCQ":
            return st.radio("Wählen Sie eine Antwort:", options, key=f"mcq_{index}")
        elif qtype == "Checkbox":
            return st.multiselect("Wählen Sie alle richtigen Antworten:", options, key=f"chk_{index}")
        elif qtype == "Matching":
            st.info("Bitte geben Sie die passende Zuordnung ein (z. B.: A → 1, B → 2…)")
            return st.text_input("Ihre Zuordnung:", key=f"match_{index}")
        elif qtype == "Sequence":
            st.info("Bitte geben Sie die richtige Reihenfolge ein, z. B.: 1–2–3–4")
            return st.text_input("Reihenfolge:", key=f"seq_{index}")
        else:
            st.warning("❗ Unbekannter Fragetyp")
            return ""

    for i, row in df.iterrows():
        user_answer = render_question(row, i)
        user_answers.append((row['Correct Answer(s)'], user_answer))

    if st.button("✅ Quiz auswerten"):
        for i, (correct, given) in enumerate(user_answers):
            st.markdown(f"#### Frage {i + 1}:")
            correct_str = str(correct).strip().lower()
            given_str = ', '.join(sorted(given)).lower() if isinstance(given, list) else str(given).strip().lower()
            if correct_str == given_str:
                st.success("✔️ Richtig")
                score += 1
            else:
                st.error(f"❌ Falsch – Richtige Antwort: {correct}")

        st.markdown(f"## 🧾 Ergebnis: {score} von {len(user_answers)} Punkten")
else:
    st.stop()
