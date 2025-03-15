#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psycopg2
import json

# Afficher une chanson avec ses détails
def view_chanson(conn, chanson_id):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT Chanson.id, Chanson.titre, Chanson.durée, Chanson.genre, Artiste.nom AS auteur, 
                   (SELECT json_agg(Artiste.nom) FROM CompositeurDroit 
                    JOIN Artiste ON CompositeurDroit.compositeur = Artiste.id 
                    WHERE CompositeurDroit.contrat = DroitAuteur.id) AS compositeurs,
                   (SELECT json_agg(Artiste.nom) FROM ArtisteDroit
                    JOIN Artiste ON ArtisteDroit.artiste = Artiste.id
                    WHERE ArtisteDroit.contrat = DroitAuteur.id) AS auteurs,
                   DroitAuteur.editeurs
            FROM Chanson
            JOIN DroitAuteur ON Chanson.id = DroitAuteur.chanson
            LEFT JOIN Artiste ON Chanson.auteur = Artiste.id
            WHERE Chanson.id = %s
        """, (chanson_id,))
        chanson = cursor.fetchone()
        if chanson:
            print("ID :", chanson[0])
            print("Titre :", chanson[1])
            print("Durée :", chanson[2])
            print("Genre :", chanson[3])
            print("Auteur :", chanson[4])
            print("Compositeurs :", chanson[5])
            print("Auteurs :", chanson[6])
            print("Éditeurs :", chanson[7])
        else:
            print("Chanson non trouvée")

# Afficher toutes les chansons
def view_all_chansons(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, titre, durée, genre, auteur, album FROM Chanson
        """)
        chansons = cursor.fetchall()
        if chansons:
            print("Toutes les chansons :")
            for chanson in chansons:
                print(f"ID : {chanson[0]}, Titre : {chanson[1]}, Durée : {chanson[2]}, Genre : {chanson[3]}, Auteur : {chanson[4]}, Album : {chanson[5]}")
        else:
            print("Aucune chanson trouvée")

# Créer une chanson
def create_chanson(conn):
    id = int(input("Id : "))
    titre = input("Titre de la chanson : ")
    duree = input("Durée de la chanson (format HH:MM:SS) : ")
    auteur_id = input("ID de l'auteur : ")
    album_id = input("ID de l'album : ")
    genre = input("Genre de la chanson : ")

    compositeur_ids = input("IDs des compositeurs (séparés par des virgules) : ").split(',')
    compositeur_ids = [int(id.strip()) for id in compositeur_ids]

    auteur_ids = input("IDs des auteurs (séparés par des virgules) : ").split(',')
    auteur_ids = [int(id.strip()) for id in auteur_ids]

    editeurs = input("Éditeurs (format JSON) : ")
    try:
        editeurs_list = json.loads(editeurs)
        if len(editeurs_list) < 1:
            raise ValueError("Il doit y avoir au moins un éditeur.")
    except json.JSONDecodeError:
        print("Format JSON invalide pour les éditeurs.")
        return
    except ValueError as e:
        print(e)
        return

    with conn.cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO Chanson (id, titre, durée, auteur, album, genre) VALUES (%i, %s, %s, %s, %s, %s) RETURNING id",
                (id, titre, duree, auteur_id, album_id, genre)
            )
            chanson_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO DroitAuteur (chanson, editeurs) VALUES (%s, %s) RETURNING id",
                (chanson_id, json.dumps(editeurs_list))
            )
            droit_auteur_id = cursor.fetchone()[0]

            for compositeur_id in compositeur_ids:
                cursor.execute(
                    "INSERT INTO CompositeurDroit (compositeur, contrat) VALUES (%s, %s)",
                    (compositeur_id, droit_auteur_id)
                )
            for auteur_id in auteur_ids:
                cursor.execute(
                    "INSERT INTO ArtisteDroit (artiste, contrat) VALUES (%s, %s)",
                    (auteur_id, droit_auteur_id)
                )

            conn.commit()
            print(f"Chanson '{titre}' créée avec succès avec ID {chanson_id}")
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Erreur d'intégrité :", e)
        except Exception as e:
            conn.rollback()
            print("Erreur lors de la création de la chanson :", e)

# Modifier une chanson
def modify_chanson(conn):
    chanson_id = input("ID de la chanson à modifier : ")

    with conn.cursor() as cursor:
        cursor.execute("SELECT titre, duree, auteur, album, genre FROM Chanson WHERE id = %s", (chanson_id,))
        chanson = cursor.fetchone()
        if chanson:
            print(f"Chanson actuelle : Titre = {chanson[0]}, Durée = {chanson[1]}, Auteur = {chanson[2]}, Album = {chanson[3]}, Genre = {chanson[4]}")

            nouveau_titre = input("Nouveau titre (laisser vide pour ne pas changer) : ")
            nouvelle_duree = input("Nouvelle durée (laisser vide pour ne pas changer) : ")
            nouvel_auteur_id = input("Nouvel ID de l'auteur (laisser vide pour ne pas changer) : ")
            nouvel_album_id = input("Nouvel ID de l'album (laisser vide pour ne pas changer) : ")
            nouveau_genre = input("Nouveau genre (laisser vide pour ne pas changer) : ")

            try:
                if nouveau_titre:
                    cursor.execute("UPDATE Chanson SET titre = %s WHERE id = %s", (nouveau_titre, chanson_id))
                if nouvelle_duree:
                    cursor.execute("UPDATE Chanson SET duree = %s WHERE id = %s", (nouvelle_duree, chanson_id))
                if nouvel_auteur_id:
                    cursor.execute("UPDATE Chanson SET auteur = %s WHERE id = %s", (nouvel_auteur_id, chanson_id))
                if nouvel_album_id:
                    cursor.execute("UPDATE Chanson SET album = %s WHERE id = %s", (nouvel_album_id, chanson_id))
                if nouveau_genre:
                    cursor.execute("UPDATE Chanson SET genre = %s WHERE id = %s", (nouveau_genre, chanson_id))

                conn.commit()
                print(f"Chanson {chanson_id} mise à jour avec succès.")
            except psycopg2.IntegrityError as e:
                conn.rollback()
                print("Erreur d'intégrité :", e)
            except Exception as e:
                conn.rollback()
                print("Erreur lors de la modification de la chanson :", e)
        else:
            print("Chanson non trouvée")

# Supprimer une chanson
def delete_chanson(conn, chanson_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM CompositeurDroit WHERE contrat IN (SELECT id FROM DroitAuteur WHERE chanson = %s)", (chanson_id,))
            cursor.execute("DELETE FROM ArtisteDroit WHERE contrat IN (SELECT id FROM DroitAuteur WHERE chanson = %s)", (chanson_id,))
            cursor.execute("DELETE FROM DroitAuteur WHERE chanson = %s", (chanson_id,))
            cursor.execute("DELETE FROM Chanson WHERE id = %s", (chanson_id,))
            conn.commit()
            print(f"Chanson avec ID {chanson_id} supprimée avec succès")
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Erreur d'intégrité :", e)
        except Exception as e:
            conn.rollback()
            print("Erreur lors de la suppression de la chanson :", e)

# Modifier un droit d'auteur
def modify_droit_auteur(conn):
    droit_auteur_id = input("ID du droit d'auteur à modifier : ")

    with conn.cursor() as cursor:
        while True:
            print("\nQue voulez-vous faire ?")
            print("1. Modifier les éditeurs")
            print("2. Modifier les compositeurs")
            print("3. Modifier les auteurs")
            print("4. Quitter")

            choix = input("Entrez votre choix : ")

            if choix == '1':
                cursor.execute("SELECT editeurs FROM DroitAuteur WHERE id = %s", (droit_auteur_id,))
                current_editeurs = cursor.fetchone()[0]
                print(f"Éditeurs actuels : {current_editeurs}")

                while True:
                    print("\nQue voulez-vous faire avec les éditeurs ?")
                    print("1. Ajouter un éditeur")
                    print("2. Supprimer un éditeur")
                    print("3. Modifier un éditeur")
                    print("4. Quitter")

                    choix_editeur = input("Entrez votre choix : ")

                    if choix_editeur == '1':
                        editeur = input("Nouvel éditeur à ajouter (format JSON) : ")
                        try:
                            editeurs_list = json.loads(current_editeurs)
                            editeurs_list.append(json.loads(editeur))
                            new_editeurs = json.dumps(editeurs_list)
                            cursor.execute("UPDATE DroitAuteur SET editeurs = %s WHERE id = %s", (new_editeurs, droit_auteur_id))
                            conn.commit()
                            print(f"Nouvel éditeur ajouté avec succès au droit d'auteur {droit_auteur_id}")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Erreur d'intégrité :", e)
                        except Exception as e:
                            conn.rollback()
                            print("Erreur lors de l'ajout de l'éditeur :", e)

                    elif choix_editeur == '2':
                        editeur_nom = input("Nom de l'éditeur à supprimer : ")
                        try:
                            editeurs_list = json.loads(current_editeurs)
                            editeurs_list = [ed for ed in editeurs_list if ed['nom'] != editeur_nom]
                            if len(editeurs_list) < 1:
                                raise Exception("Il doit y avoir au moins un éditeur par contrat.")
                            new_editeurs = json.dumps(editeurs_list)
                            cursor.execute("UPDATE DroitAuteur SET editeurs = %s WHERE id = %s", (new_editeurs, droit_auteur_id))
                            conn.commit()
                            print(f"Éditeur '{editeur_nom}' supprimé avec succès du droit d'auteur {droit_auteur_id}")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Erreur d'intégrité :", e)
                        except Exception as e:
                            conn.rollback()
                            print("Erreur lors de la suppression de l'éditeur :", e)

                    elif choix_editeur == '3':
                        editeur_nom = input("Nom de l'éditeur à modifier : ")
                        nouvel_editeur = input("Nouvelle valeur de l'éditeur (format JSON) : ")
                        try:
                            editeurs_list = json.loads(current_editeurs)
                            for ed in editeurs_list:
                                if ed['nom'] == editeur_nom:
                                    ed.update(json.loads(nouvel_editeur))
                            new_editeurs = json.dumps(editeurs_list)
                            cursor.execute("UPDATE DroitAuteur SET editeurs = %s WHERE id = %s", (new_editeurs, droit_auteur_id))
                            conn.commit()
                            print(f"Éditeur '{editeur_nom}' modifié avec succès du droit d'auteur {droit_auteur_id}")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Erreur d'intégrité :", e)
                        except Exception as e:
                            conn.rollback()
                            print("Erreur lors de la modification de l'éditeur :", e)

                    elif choix_editeur == '4':
                        break

                    else:
                        print("Choix invalide. Veuillez réessayer.")

            elif choix == '2':
                while True:
                    print("\nQue voulez-vous faire avec les compositeurs ?")
                    print("1. Ajouter un compositeur")
                    print("2. Supprimer un compositeur")
                    print("3. Quitter")

                    choix_compositeur = input("Entrez votre choix : ")

                    if choix_compositeur == '1':
                        compositeur_id = input("ID du compositeur à ajouter : ")
                        try:
                            cursor.execute(
                                "INSERT INTO CompositeurDroit (compositeur, contrat) VALUES (%s, %s)",
                                (compositeur_id, droit_auteur_id)
                            )
                            conn.commit()
                            print(f"Compositeur {compositeur_id} ajouté avec succès au droit d'auteur {droit_auteur_id}")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Erreur d'intégrité :", e)
                        except Exception as e:
                            conn.rollback()
                            print("Erreur lors de l'ajout du compositeur :", e)

                    elif choix_compositeur == '2':
                        compositeur_id = input("ID du compositeur à supprimer : ")
                        try:
                            cursor.execute(
                                "DELETE FROM CompositeurDroit WHERE compositeur = %s AND contrat = %s",
                                (compositeur_id, droit_auteur_id)
                            )
                            conn.commit()
                            print(f"Compositeur {compositeur_id} supprimé avec succès du droit d'auteur {droit_auteur_id}")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Erreur d'intégrité :", e)
                        except Exception as e:
                            conn.rollback()
                            print("Erreur lors de la suppression du compositeur :", e)

                    elif choix_compositeur == '3':
                        break

                    else:
                        print("Choix invalide. Veuillez réessayer.")

            elif choix == '3':
                while True:
                    print("\nQue voulez-vous faire avec les auteurs ?")
                    print("1. Ajouter un auteur")
                    print("2. Supprimer un auteur")
                    print("3. Quitter")

                    choix_auteur = input("Entrez votre choix : ")

                    if choix_auteur == '1':
                        auteur_id = input("ID de l'auteur à ajouter : ")
                        try:
                            cursor.execute(
                                "INSERT INTO ArtisteDroit (artiste, contrat) VALUES (%s, %s)",
                                (auteur_id, droit_auteur_id)
                            )
                            conn.commit()
                            print(f"Auteur {auteur_id} ajouté avec succès au droit d'auteur {droit_auteur_id}")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Erreur d'intégrité :", e)
                        except Exception as e:
                            conn.rollback()
                            print("Erreur lors de l'ajout de l'auteur :", e)

                    elif choix_auteur == '2':
                        auteur_id = input("ID de l'auteur à supprimer : ")
                        try:
                            cursor.execute(
                                "DELETE FROM ArtisteDroit WHERE artiste = %s AND contrat = %s",
                                (auteur_id, droit_auteur_id)
                            )
                            conn.commit()
                            print(f"Auteur {auteur_id} supprimé avec succès du droit d'auteur {droit_auteur_id}")
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print("Erreur d'intégrité :", e)
                        except Exception as e:
                            conn.rollback()
                            print("Erreur lors de la suppression de l'auteur :", e)

                    elif choix_auteur == '3':
                        break

                    else:
                        print("Choix invalide. Veuillez réessayer.")

            elif choix == '4':
                break

            else:
                print("Choix invalide. Veuillez réessayer.")

def main(conn):

    while True:
        print("\nQue voulez-vous faire ?")
        print("1. Afficher une chanson")
        print("2. Afficher toutes les chansons")
        print("3. Créer une chanson")
        print("4. Modifier une chanson")
        print("5. Supprimer une chanson")
        print("6. Supprimer toutes les chansons")
        print("7. Modifier un droit d'auteur")
        print("8. Quitter")

        choix = input("Entrez votre choix : ")

        if choix == '1':
            chanson_id = int(input("ID de la chanson : "))
            view_chanson(conn, chanson_id)
        elif choix == '2':
            view_all_chansons(conn)
        elif choix == '3':
            create_chanson(conn)
        elif choix == '4':
            modify_chanson(conn)
        elif choix == '5':
            chanson_id = int(input("ID de la chanson à supprimer : "))
            delete_chanson(conn, chanson_id)
        #elif choix == '6':
            #delete_all_chansons(conn)
        elif choix == '7':
            modify_droit_auteur(conn)
        elif choix == '8':
            break
        else:
            print("Choix invalide. Veuillez réessayer.")



