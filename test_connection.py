import psycopg2

try:
    conn = psycopg2.connect(
        dbname="iset_chatbot",
        user="postgres",
        password="Sirine123@",
        host="127.0.0.1",
        port="5432"
    )
    print("✅ Connexion réussie !")
    conn.close()
except Exception as e:
    print("❌ Erreur :", e)
