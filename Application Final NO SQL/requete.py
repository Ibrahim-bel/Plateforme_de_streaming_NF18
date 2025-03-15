import psycopg2
from collections import Counter

# Fonction pour demander oui ou non
def ouinon(question):
    response = input(question)
    if response.lower() != 'oui' and response.lower() != 'non':
        ouinon(question)
    return response

# Fonction principale pour exécuter les requêtes
def main(conn):
    cursor = conn.cursor()

    # Requête 1 : Durée moyenne des chansons par artiste ayant au moins 5 chansons
    reponse = ouinon('Voulez-vous connaitre la durée moyenne des chansons par artiste ? ')
    if reponse == 'oui':
        try:
            cursor.execute("""
                SELECT a.nom, TO_CHAR(AVG(c.durée), 'HH24:MI:SS') AS duree_moyenne
                FROM Chanson c
                JOIN Artiste a ON c.auteur = a.id
                GROUP BY a.id
                HAVING COUNT(*) >= 5;
            """)
            results = cursor.fetchall()
            print("Durée moyenne des chansons par artiste :")
            for x in results:
                print(x)

        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Message système :", e)

    # Requête 2 : Artiste avec le plus de chansons
    reponse = ouinon("Voulez-vous connaitre l'artiste avec le plus de chansons ? ")
    if reponse == 'oui':
        try:
            cursor.execute("""
                SELECT a.nom, COUNT(c.auteur) AS nombre_chansons
                FROM Chanson c
                JOIN Artiste a ON c.auteur = a.id
                GROUP BY a.id
                ORDER BY COUNT(*) DESC
                LIMIT 1;
            """)
            results = cursor.fetchall()
            print("Artiste avec le plus de chansons :")
            for x in results:
                print(x)

        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Message système :", e)

    # Requête 3 : Artistes avec les chansons les plus longues (durée > 10 min)
    reponse = ouinon('Voulez-vous connaitre les artistes avec les chansons les plus longues (durée > 10 min) ? ')
    if reponse == 'oui':
        try:
            cursor.execute("""
                SELECT DISTINCT a.nom, c.titre, TO_CHAR(c.durée, 'HH24:MI:SS')
                FROM Chanson c
                JOIN Artiste a ON c.auteur = a.id
                WHERE c.durée >= '00:10:00';
            """)
            results = cursor.fetchall()
            print("Artistes avec les chansons les plus longues (durée > 10 min) :")
            for x in results:
                print(x)

        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Message système :", e)

    # Requête 4 : Genres préférés des artistes par les utilisateurs
    reponse = ouinon('Voulez-vous connaitre les genres préférés des artistes par les utilisateurs ? ')
    if reponse == 'oui':
        try:
            # cursor.execute("""
            #     SELECT genre, COUNT(*) AS nombre_utilisateurs
            #     FROM Utilisateur u, jsonb_array_elements_text(u.preferences) AS genre
            #     GROUP BY genre
            #     ORDER BY COUNT(*) DESC;
            # """)

            cursor.execute("""
                SELECT JSON_ARRAY_ELEMENTS(preferences) AS genre
                FROM Utilisateur
            """)

            results = cursor.fetchall()
            genre_counts = Counter(results)
            sorted_genre_counts = genre_counts.most_common()
            for genre, count in sorted_genre_counts:
                print(f"{genre}: {count}")
            

            """ print("Genres préférés des artistes par les utilisateurs :")
            for x in results:
                print(x) """

        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Message système :", e)

