import json
from neo4j import GraphDatabase

# Connexion à Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "781227pAssWord!"

driver = GraphDatabase.driver(uri, auth=(username, password))

# Charger le fichier JSON depuis la racine du projet
with open('filler/act.json', 'r', encoding='utf-8') as f:
    questions_data = json.load(f)

with open('filler/act-score.json', 'r', encoding='utf-8') as f:
    score_data = json.load(f)



# Fonction pour créer les noeuds et relations dans Neo4j
def create_asthma_questionnaire(tx, data):
    # Créer le node Maladie : Asthme
    tx.run("MERGE (m:Maladie {nom: 'Asthme'})")

    # Créer le node Questionnaire : ACT
    tx.run("""
        MERGE (q:Questionnaire {nom: 'ACT'})
        WITH q
        MATCH (m:Maladie {nom: 'Asthme'})
        MERGE (m)-[:A_POUR_QUESTIONNAIRE]->(q)
    """)

    # Ajouter les questions et propositions
    for i, question in enumerate(data["questions"], 1):
        question_text = question["question"]
        tx.run("""
            MATCH (q:Questionnaire {nom: 'ACT'})
            MERGE (ques:Question {text: $text, numero: $numero})
            MERGE (q)-[:A_POUR_QUESTION]->(ques)
        """, text=question_text, numero=i)

        # Ajouter les propositions liées à chaque question
        for option in question["options"]:
            tx.run("""
                MATCH (ques:Question {text: $text})
                MERGE (prop:Proposition {label: $label, score: $score})
                MERGE (ques)-[:A_POUR_PROPOSITION]->(prop)
            """, text=question_text, label=option["label"], score=option["score"])
# Fonction pour créer les noeuds SCORE et les relier au Questionnaire ACT
def create_score_nodes(tx, data):
    # Créer le node Questionnaire : ACT s'il n'existe pas déjà
    tx.run("""
        MERGE (q:Questionnaire {nom: 'ACT'})
    """)

    # Ajouter les scores et les relier au Questionnaire
    for score_entry in data:
        score_range = score_entry["score"]
        interpretation = score_entry["interpretation"]
        intervention = score_entry["intervention"]

        tx.run("""
            MATCH (q:Questionnaire {nom: 'ACT'})
            MERGE (s:Score {range: $range, interpretation: $interpretation, intervention: $intervention})
            MERGE (q)-[:A_POUR_SCORE]->(s)
        """, range=score_range, interpretation=interpretation, intervention=intervention)

# Insérer les données dans Neo4j
with driver.session() as session:
    session.execute_write(create_asthma_questionnaire, questions_data)
    session.execute_write(create_score_nodes, score_data)

# Fermeture de la connexion
driver.close()




