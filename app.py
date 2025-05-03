from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from chatbot.dataset import load_intents
from chatbot.model import train_model, predict_class
from chatbot.database import check_postgresql_connection

# Téléchargement des ressources NLTK nécessaires
nltk.download('punkt')
nltk.download('wordnet')

# Création de l'application Flask
app = Flask(__name__)
CORS(app)

# Vérification de la connexion PostgreSQL
if not check_postgresql_connection():
    print("❌ Connexion à PostgreSQL échouée. Veuillez vérifier vos paramètres.")
    exit(1)

# Chargement des intents depuis la base PostgreSQL
intents = load_intents()

# Vérification que des intents sont présents
if not intents:
    print("❌ Aucune donnée d'entraînement trouvée dans la base de données.")
    exit(1)

# Entraînement du modèle de classification
try:
    model, tags = train_model(intents)
except ValueError as e:
    print(f"❌ Erreur pendant l'entraînement du modèle : {e}")
    exit(1)

# Route API pour gérer les requêtes utilisateur
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Message vide"}), 400

    tag = predict_class(message, model, tags, intents)
    return jsonify({"response": tag})

# Lancement de l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
