import psycopg2

# Fonction pour ajouter une collaboration entre un album et un artiste invité
def ajouter_collaboration(conn, album_id, artiste_invite_id):
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO Collaboration (album, artisteInvité) VALUES (%s, %s)", (album_id, artiste_invite_id))
        conn.commit()
        print("Collaboration ajoutée avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Erreur d'intégrité :", e)

# Fonction pour supprimer une collaboration entre un album et un artiste invité
def supprimer_collaboration(conn, album_id, artiste_invite_id):
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM Collaboration WHERE album = %s AND artisteInvité = %s", (album_id, artiste_invite_id))
        conn.commit()
        print("Collaboration supprimée avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Erreur d'intégrité :", e)

# Fonction pour afficher les collaborations d'un artiste
def afficher_collaborations_artiste(conn, album_id):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM Collaboration as c
                JOIN Artiste as a ON c.artisteInvité = a.id
                WHERE album = {album_id}""")
    collaborations = cursor.fetchall()
    for collaboration in collaborations:
        print(collaboration)

def afficher_collaborations(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Collaboration")
    collaborations = cursor.fetchall()
    print("\nCollaborations :")
    for collaboration in collaborations:
        print(collaboration)

# Fonction principale
def main(conn):
        while True:
            print("\nQue souhaitez-vous faire ?")
            print("1. Ajouter une collaboration")
            print("2. Supprimer une collaboration")
            print("3. Afficher les collaborations d'un album")
            print("4. Afficher toutes les collaborations")
            print("5. Quitter")

            choix = input("Entrez le numéro de votre choix : ")

            if choix == "1":
                album_id = int(input("Entrez l'ID de l'album : "))
                artiste_invite_id = int(input("Entrez l'ID de l'artiste invité : "))
                ajouter_collaboration(conn, album_id, artiste_invite_id)
            elif choix == "2":
                album_id = int(input("Entrez l'ID de l'album : "))
                artiste_invite_id = int(input("Entrez l'ID de l'artiste invité : "))
                supprimer_collaboration(conn, album_id, artiste_invite_id)
            elif choix == "3":
                album_id = int(input("Entrez l'ID de l'album : "))
                afficher_collaborations_artiste(conn, album_id)
            
            elif choix == "4":
                afficher_collaborations(conn)

            elif choix == "5":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Veuillez entrer un numéro valide.")
        return
