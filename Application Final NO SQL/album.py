import psycopg2

def insert(conn):
    cursor = conn.cursor()
    
    
    id = int(input("Id : "))
    titre = input("Titre : ")
    annee = int(input("Année de sortie : "))
    sql = f"INSERT INTO Album(id, titre, annéeSortie) VALUES ({id}, '{titre}', {annee})"
    
    try :
        cursor.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def display(conn):
    cursor = conn.cursor()
    try :
        cursor.execute("SELECT * FROM Album")
        results = cursor.fetchall()
        for x in results:
            print(x)

    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def afficher_chansons_album(conn):
    cursor = conn.cursor()
    try :
        val = int(input("Insérer id de l'album : "))
        cursor.execute(f"""SELECT c.id, c.titre, TO_CHAR(c.durée, 'HH24:MI:SS'), c.album, c.auteur, c.genre FROM Chanson as c 
                WHERE c.album = {val}""")
        results = cursor.fetchall()
        print("(id, titre, durée, album, auteur, genre)")
        for x in results:
            print(x)

    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)


def delete(conn):
    cursor = conn.cursor()
    val = int(input("Inserer l'id de l'album que vous voulez supprimer : "))
    sql = f"DELETE FROM Album WHERE id = {val}"
    try :
        cursor.execute(sql)
        conn.commit()
        print("Album supprimé avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)


def deleteAll(conn):
    cursor = conn.cursor()
    sql = "DELETE FROM Album"
    try :
        cursor.execute(sql)
        conn.commit()
        print("Tous les albums supprimés avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)


def update(conn):
    cursor = conn.cursor()
    id = int(input("Inserer l'id de l'album que vous voulez modifier : "))
    column_index = int(input("Choisissez la column à modifier. Titre : 0, annéeSortie: 1 "))
 
    if column_index == 0:
        val = input("Quelles donnée voulez vous insérer en remplacement? ")
        sql = f"UPDATE Album SET titre = '{val}' WHERE id = {id}"
    elif column_index == 1:
        val = input("Quelles donnée voulez vous insérer en remplacement?")
        sql = f"UPDATE Album SET annéesortie = {val} WHERE id = {id}"
    else:
        print('Colonne invalide !')
        return

    try :
        cursor.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def main(conn):

    i = 0
    while i != 1:
        print("\nQue souhaitez-vous faire ?")
        print("1. Ajouter un album")
        print("2. Modifier un album")
        print("3. Afficher tous les albums")
        print("4. Afficher les chansons d'un album")
        print("5. Supprimer tous les albums")
        print("6. Supprimer un album")
        print("7. Quitter")
        type = int(input("Saisir le numéro correspondant à votre choix : "))
        if type == 1:
            insert(conn)
        elif type == 2:
            update(conn)
        elif type == 3:
            display(conn)
        elif type == 4:
            afficher_chansons_album(conn)
        elif type == 5:
            deleteAll(conn)
        elif type == 6:
            delete(conn)
        elif type == 7:
            i = 1
        else:
            print("Choix invalide")

    return
