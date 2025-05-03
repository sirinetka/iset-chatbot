import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Télécharger les stopwords (à exécuter une seule fois)
nltk.download('stopwords', quiet=True)

# Choisir la langue des stopwords
stop_words = set(stopwords.words('french'))  # Change en 'english' si besoin
stemmer = PorterStemmer()

def preprocess_text(text):  # Fonction renommée en 'preprocess_text'
    # Mise en minuscule
    text = text.lower()
    
    # Suppression des caractères spéciaux
    text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
    
    # Tokenisation
    tokens = text.split()
    
    # Suppression des stopwords + stemming
    filtered_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]
    
    return " ".join(filtered_tokens)
