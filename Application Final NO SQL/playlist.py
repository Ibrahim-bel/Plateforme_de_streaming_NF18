#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import json

def insert(conn):
    cursor = conn.cursor()
    
    id = int(input("Id : "))
    titre = input("Titre : ")
    description = input("Description : ")
    autorisation_acces = select_access_permission()
    createur = int(input("Créateur (ID) : "))
    
    chansons = []
    while True:
        chanson_id = input("Ajouter l'ID d'une chanson (ou appuyer sur entrée pour terminer) : ")
        if chanson_id == "":
            break
        chansons.append(int(chanson_id))
    
    albums = []
    while True:
        album_id = input("Ajouter l'ID d'un album (ou appuyer sur entrée pour terminer) : ")
        if album_id == "":
            break
        albums.append(int(album_id))
    
    info_playlist = {"titre": titre, "description": description}
    
    sql = f"INSERT INTO Playlist(id, info_playlist, autorisationAcces, créateur, chansons, albums) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (id, json.dumps(info_playlist), autorisation_acces, createur, json.dumps(chansons), json.dumps(albums))
    
    try:
        cursor.execute(sql, data)
        conn.commit()
        print("Playlist insérée avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def display(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Playlist")
        results = cursor.fetchall()
        print("(id_playlist, info_playlist, autorisationAcces, créateur, chansons, albums)")
        for x in results:
            print(x)
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def delete(conn):
    cursor = conn.cursor()
    val = int(input("Insérer l'id de la playlist que vous voulez supprimer : "))
    sql = f"DELETE FROM Playlist WHERE id = %s"
    try:
        cursor.execute(sql, (val,))
        conn.commit()
        print("Playlist supprimée avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def deleteAll(conn):
    cursor = conn.cursor()
    sql = "DELETE FROM Playlist"
    try:
        cursor.execute(sql)
        conn.commit()
        print("Toutes les playlists ont été supprimées avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def update(conn):
    cursor = conn.cursor()
    id = int(input("Insérer l'id de la playlist que vous voulez modifier : "))
    print("1. Modifier le titre")
    print("2. Modifier la description")
    print("3. Modifier l'autorisation d'accès")
    print("4. Ajouter une chanson")
    print("5. Supprimer une chanson")
    print("6. Ajouter un album")
    print("7. Supprimer un album")
    choice = int(input("Choisissez l'opération à effectuer : "))
    
    if choice == 1:
        val = input("Nouveau titre : ")
        sql = f"UPDATE Playlist SET info_playlist = jsonb_set(info_playlist, '{{titre}}', %s) WHERE id = %s"
        data = (json.dumps(val), id)
    elif choice == 2:
        val = input("Nouvelle description : ")
        sql = f"UPDATE Playlist SET info_playlist = jsonb_set(info_playlist, '{{description}}', %s) WHERE id = %s"
        data = (json.dumps(val), id)
    elif choice == 3:
        val = select_access_permission()
        sql = f"UPDATE Playlist SET autorisationAcces = %s WHERE id = %s"
        data = (val, id)
    elif choice == 4:
        chanson_id = int(input("ID de la chanson à ajouter : "))
        cursor.execute("SELECT chansons FROM Playlist WHERE id = %s", (id,))
        current_chansons = json.loads(cursor.fetchone()[0])
        current_chansons.append(chanson_id)
        sql = "UPDATE Playlist SET chansons = %s WHERE id = %s"
        data = (json.dumps(current_chansons), id)
    elif choice == 5:
        chanson_id = int(input("ID de la chanson à supprimer : "))
        cursor.execute("SELECT chansons FROM Playlist WHERE id = %s", (id,))
        current_chansons = json.loads(cursor.fetchone()[0])
        if chanson_id in current_chansons:
            current_chansons.remove(chanson_id)
        sql = "UPDATE Playlist SET chansons = %s WHERE id = %s"
        data = (json.dumps(current_chansons), id)
    elif choice == 6:
        album_id = int(input("ID de l'album à ajouter : "))
        cursor.execute("SELECT albums FROM Playlist WHERE id = %s", (id,))
        current_albums = json.loads(cursor.fetchone()[0])
        current_albums.append(album_id)
        sql = "UPDATE Playlist SET albums = %s WHERE id = %s"
        data = (json.dumps(current_albums), id)
    elif choice == 7:
        album_id = int(input("ID de l'album à supprimer : "))
        cursor.execute("SELECT albums FROM Playlist WHERE id = %s", (id,))
        current_albums = json.loads(cursor.fetchone()[0])
        if album_id in current_albums:
            current_albums.remove(album_id)
        sql = "UPDATE Playlist SET albums = %s WHERE id = %s"
        data = (json.dumps(current_albums), id)
    else:
        print('Choix invalide !')
        return

    try:
        cursor.execute(sql, (data))
        conn.commit()
        print("Playlist mise à jour avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def select_access_permission():
    while True:
        print("Sélectionnez l'autorisation d'accès :")
        print("1. Privée")
        print("2. Publique")
        print("3. Partagée avec des amis")
        choix = input("Votre choix (1/2/3) : ")
        if choix == "1":
            return "privée"
        elif choix == "2":
            return "publique"
        elif choix == "3":
            return "partagée avec des amis"
        else:
            print("Choix invalide. Veuillez choisir 1, 2 ou 3.")

def afficher_playlist(conn):
    cursor = conn.cursor()
    playlist_id = int(input("Entrez l'ID de la playlist à afficher : "))
    
    try:
        cursor.execute("""
            SELECT p.id, p.info_playlist->>'titre' AS titre_playlist, p.info_playlist->>'description' AS description, 
                   p.autorisationAcces, p.créateur, 
                   c.id AS chanson_id, c.titre AS titre_chanson, 
                   a.id AS album_id
            FROM Playlist AS p
            LEFT JOIN LATERAL jsonb_to_recordset(p.chansons) AS c(id INT, titre VARCHAR)
            ON TRUE
            LEFT JOIN LATERAL jsonb_to_recordset(p.albums) AS a(id INT, titre VARCHAR)
            ON TRUE
            WHERE p.id = %s
        """, (playlist_id,))
        
        result = cursor.fetchone()
        if result:
            print("\nPlaylist trouvée :")
            print(f"ID : {result[0]}")
            print(f"Titre : {result[1]}")
            print(f"Description : {result[2]}")
            print(f"Autorisation d'accès : {result[3]}")
            print(f"Créateur (ID) : {result[4]}")
            print("\nChansons :")
            while result[5] is not None:
                print(f"  - ID : {result[5]}, Titre : {result[6]}")
                result = cursor.fetchone()
            print("\nAlbums :")
            while result[7] is not None:
                print(f"  - ID : {result[7]}, Titre : {result[8]}")
                result = cursor.fetchone()
        else:
            print(f"Aucune playlist trouvée avec l'ID {playlist_id}")

    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def main(conn):
    while True:
        print("\nQue souhaitez-vous faire ?")
        print("1. Ajouter une playlist")
        print("2. Modifier une playlist")
        print("3. Afficher toutes les playlists")
        print("4. Afficher une playlist")
        print("5. Supprimer toutes les playlists")
        print("6. Supprimer une playlist")
        print("7. Quitter")
        choix = int(input("Saisir le numéro correspondant à votre choix : "))
        
        if choix == 1:
            insert(conn)
        elif choix == 2:
            update(conn)
        elif choix == 3:
            display(conn)
        elif choix == 4:
            afficher_playlist(conn)
        elif choix == 5:
            deleteAll(conn)
        elif choix == 6:
            delete(conn)
        elif choix == 7:
            break
        else:
            print("Choix invalide")

    conn.close()
    print("Programme terminé.")