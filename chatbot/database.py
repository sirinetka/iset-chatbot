from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import psycopg2
import urllib.parse

# Configuration PostgreSQL
DB_USER = "postgres"
DB_PASSWORD = "Sirine123@"  # Mot de passe avec caractères spéciaux
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "iset_chatbot"

# Encodage du mot de passe pour l'URL de connexion
DB_PASSWORD_ENCODED = urllib.parse.quote(DB_PASSWORD)

# Création de l'URL de connexion avec le mot de passe encodé
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}?hostaddr={DB_HOST}"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Vérification de la connexion
def check_postgresql_connection():
    try:
        with engine.connect() as connection:
            print("✅ Connexion à PostgreSQL réussie.")
            return True
    except OperationalError as e:
        print("❌ Connexion à PostgreSQL échouée. Veuillez vérifier vos paramètres.")
        print("Détail :", e)
        return False
