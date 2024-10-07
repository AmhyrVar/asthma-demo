from fastapi import FastAPI
from neo4j import GraphDatabase
from typing import List, Optional

# Connexion à Neo4j
uri = "bolt://neo4j:7687"
username = "neo4j"
password = "781227pAssWord!"

driver = GraphDatabase.driver(uri, auth=(username, password))

app = FastAPI()

# Fonction pour récupérer les maladies disponibles
@app.get("/maladies")
def get_maladies():
    with driver.session() as session:
        result = session.run("MATCH (m:Maladie) RETURN m.nom AS nom")
        maladies = [record["nom"] for record in result]
    return maladies

# Fonction pour récupérer les questionnaires liés à une maladie
@app.get("/questionnaires")
def get_questionnaires(maladie: str):
    with driver.session() as session:
        result = session.run("""
            MATCH (m:Maladie {nom: $maladie})-[:A_POUR_QUESTIONNAIRE]->(q:Questionnaire)
            RETURN q.nom AS nom
        """, maladie=maladie)
        questionnaires = [record["nom"] for record in result]
    return questionnaires

# Fonction pour récupérer les questions liées à un questionnaire
@app.get("/questions")
def get_questions(questionnaire: str):
    with driver.session() as session:
        result = session.run("""
            MATCH (q:Questionnaire {nom: $questionnaire})-[:A_POUR_QUESTION]->(ques:Question)
            RETURN ques.text AS question, ques.numero AS numero
            ORDER BY ques.numero
        """, questionnaire=questionnaire)
        questions = [{"numero": record["numero"], "question": record["question"]} for record in result]
    return questions

# Fonction pour récupérer les propositions pour une question
@app.get("/propositions")
def get_propositions(question_text: str):
    with driver.session() as session:
        result = session.run("""
            MATCH (ques:Question {text: $text})-[:A_POUR_PROPOSITION]->(prop:Proposition)
            RETURN prop.label AS label, prop.score AS score
        """, text=question_text)
        propositions = [{"label": record["label"], "score": record["score"]} for record in result]
    return propositions



# Fonction pour récupérer les scores et leurs interprétations
@app.get("/score_interpretation")
def get_score_interpretation(total_score: int):
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Score)
            WHERE (
                s.range = '<15' AND $total_score < 15
            ) OR (
                s.range = '15-19' AND $total_score >= 15 AND $total_score <= 19
            ) OR (
                s.range = '20-25' AND $total_score >= 20 AND $total_score <= 25
            )
            RETURN s.interpretation AS interpretation, s.intervention AS intervention
        """, total_score=total_score)
        
        record = result.single()
        if record:
            return {"interpretation": record["interpretation"], "intervention": record["intervention"]}
        return {"interpretation": None, "intervention": None}
