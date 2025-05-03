from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

# Fonction pour entraîner le modèle de classification
def train_model(intents):
    if not intents:
        raise ValueError("Aucune phrase d'entraînement disponible. Vérifiez les données de la base.")

    patterns = []
    responses = []
    tags = []

    for intent in intents:
        for pattern in intent['patterns']:
            patterns.append(pattern)
            responses.append(intent['responses'])
            tags.append(intent['tag'])

    # TF-IDF vectorizer pour transformer les données textuelles en vecteurs numériques
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(patterns)

    # Naive Bayes pour la classification
    model = MultinomialNB()
    model.fit(X, np.array(tags))

    return model, tags

# Fonction pour prédire la classe d'un message
def predict_class(message, model, tags, intents):
    vectorizer = TfidfVectorizer()
    X = vectorizer.transform([message])
    prediction = model.predict(X)
    predicted_tag = prediction[0]

    # Recherche de la réponse associée
    for intent in intents:
        if intent['tag'] == predicted_tag:
            return np.random.choice(intent['responses'])

    return "Désolé, je n'ai pas compris votre message."
