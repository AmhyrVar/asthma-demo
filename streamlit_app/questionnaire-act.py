import streamlit as st
import requests

# URL de base pour l'API
API_URL = "http://api:8000"

# Fonction pour récupérer les maladies depuis l'API
def get_maladies():
    response = requests.get(f"{API_URL}/maladies")
    return response.json()

# Fonction pour récupérer les questionnaires
def get_questionnaires(maladie):
    response = requests.get(f"{API_URL}/questionnaires", params={"maladie": maladie})
    return response.json()

# Fonction pour récupérer les questions
def get_questions(questionnaire):
    response = requests.get(f"{API_URL}/questions", params={"questionnaire": questionnaire})
    return response.json()

# Fonction pour récupérer les propositions
def get_propositions(question_text):
    response = requests.get(f"{API_URL}/propositions", params={"question_text": question_text})
    return response.json()

# Fonction pour récupérer l'interprétation du score
def get_score_interpretation(total_score):
    response = requests.get(f"{API_URL}/score_interpretation", params={"total_score": total_score})
    return response.json()

# Interface Streamlit
st.title("Évaluation de l'Asthme (Test ACT)")

# Étape 1 : Sélectionner la maladie
maladies = get_maladies()
maladie_selectionnee = st.selectbox("Sélectionnez une maladie", maladies)

# Étape 2 : Sélectionner le questionnaire lié
if maladie_selectionnee:
    questionnaires = get_questionnaires(maladie_selectionnee)
    questionnaire_selectionne = st.selectbox("Sélectionnez un questionnaire", questionnaires)

# Étape 3 : Affichage des questions et collecte des réponses
if questionnaire_selectionne:
    questions = get_questions(questionnaire_selectionne)
    score_total = 0
    for question in questions:
        numero = question["numero"]
        question_text = question["question"]
        st.write(f"Question {numero}: {question_text}")
        
        propositions = get_propositions(question_text)
        options = {prop["label"]: prop["score"] for prop in propositions}
        reponse = st.radio("Choisissez une réponse", options.keys(), key=numero)
        score_total += options[reponse]

    # Étape 4 : Afficher le score ACT total
    if st.button("Calculer le score ACT"):
        score_info = get_score_interpretation(score_total)
        st.write(f"Score ACT total : {score_total}")
        if score_info["interpretation"]:
            st.write(f"Interprétation : {score_info['interpretation']}")
            st.write(f"Interventions recommandées : {score_info['intervention']}")
        else:
            st.write("Aucune interprétation trouvée pour ce score.")
