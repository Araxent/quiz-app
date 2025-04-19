import streamlit as st
from pptx import Presentation
from io import BytesIO

# Lire les questions à partir d’un fichier PowerPoint
@st.cache_data
def charger_questions(uploaded_file):
    prs = Presentation(uploaded_file)
    questions = []
    for slide in prs.slides:
        question = slide.shapes.title.text if slide.shapes.title else ""
        reponse = ""
        for shape in slide.shapes:
            if shape.has_text_frame and shape != slide.shapes.title:
                reponse = shape.text
                break
        if question and reponse:
            questions.append((question.strip(), reponse.strip()))
    return questions

# --- Interface principale ---
st.set_page_config(page_title="Quiz en ligne", layout="centered")
st.title("🧠 Petit Quiz en ligne")

# 1. Upload du fichier PPTX
uploaded_file = st.file_uploader("📂 Charge ton fichier PowerPoint avec les questions", type=["pptx"])

if uploaded_file:
    questions = charger_questions(uploaded_file)

    if "pseudo" not in st.session_state:
        st.session_state.pseudo = ""
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "index" not in st.session_state:
        st.session_state.index = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "started" not in st.session_state:
        st.session_state.started = False

    if not st.session_state.pseudo:
        pseudo = st.text_input("👤 Entrez votre pseudo")
        if st.button("Se connecter") and pseudo:
            st.session_state.pseudo = pseudo
            st.experimental_rerun()
    elif not st.session_state.started:
        st.success(f"Bienvenue, {st.session_state.pseudo} !")
        if st.button("🚀 Commencer le quiz"):
            st.session_state.started = True
            st.experimental_rerun()
    else:
        if st.session_state.index < len(questions):
            question, reponse = questions[st.session_state.index]

            st.markdown(f"**Question {st.session_state.index + 1}:** {question}")

            user_answer = st.text_input("Votre réponse", key=f"rep_{st.session_state.index}")

            if st.button("Valider la réponse"):
                st.session_state.show_answer = True

            if st.session_state.show_answer:
                st.info(f"✅ Réponse correcte : {reponse}")
                if st.button("Question suivante"):
                    st.session_state.index += 1
                    st.session_state.show_answer = False
                    st.experimental_rerun()

            st.markdown("### 🎯 Score actuel")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("+1"):
                    st.session_state.score += 1
            with col3:
                if st.button("-1"):
                    st.session_state.score -= 1
            with col2:
                st.markdown(f"<h3 style='text-align: center;'>{st.session_state.score}</h3>", unsafe_allow_html=True)

        else:
            st.success("🎉 Quiz terminé !")
            st.markdown(f"**Score final de {st.session_state.pseudo} :** {st.session_state.score}")

            if st.button("🔁 Recommencer"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
