import json
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, insert
from sqlalchemy.exc import OperationalError
from sqlalchemy.dialects.postgresql import ARRAY
from chatbot.database import check_postgresql_connection

# Configuration de la base de données PostgreSQL
DB_USER = "postgres"
DB_PASSWORD = "Sirine123@"
DB_HOST = "127.0.0.1"  # Utiliser l'adresse IP locale pour éviter les problèmes de socket sous Windows
DB_PORT = "5432"
DB_NAME = "iset_chatbot"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Définition de la table "intents"
intents_table = Table(
    'intents', metadata,
    Column('id', Integer, primary_key=True),
    Column('tag', String),
    Column('patterns', ARRAY(String)),
    Column('responses', ARRAY(String))
)

# Lecture des intents depuis le fichier JSON
def load_intents_from_json():
    json_path = os.path.join(os.path.dirname(__file__), "..", "intents.json")
    with open(json_path, encoding='utf-8') as f:
        return json.load(f)

# Vérification de la connexion à PostgreSQL
def check_postgresql_connection():
    try:
        with engine.connect() as connection:
            return True
    except OperationalError:
        return False

# Chargement des intents depuis la base ou insertion si vide
def load_intents():
    try:
        with engine.connect() as connection:
            stmt = select(intents_table)
            result = connection.execute(stmt)
            rows = result.fetchall()

            if not rows:
                print("La table 'intents' est vide. Insertion depuis intents.json...")
                intents_json = load_intents_from_json()
                for intent in intents_json:
                    connection.execute(insert(intents_table).values(
                        tag=intent['tag'],
                        patterns=intent['patterns'],
                        responses=intent['responses']
                    ))
                connection.commit()
                print("Données insérées avec succès.")

                # Relecture après insertion
                result = connection.execute(select(intents_table))
                rows = result.fetchall()

            # Conversion en liste exploitable
            intents = [{
                "tag": row._mapping["tag"],
                "patterns": row._mapping["patterns"],
                "responses": row._mapping["responses"]
            } for row in rows]

            return intents

    except OperationalError as e:
        print("Erreur de connexion à la base de données :", e)
        return []

    finally:
        engine.dispose()  # Libère proprement les connexions
