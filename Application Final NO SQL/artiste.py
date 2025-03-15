#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import json

def insert(conn):
    cursor = conn.cursor()
    
    id = int(input("Id : "))
    nom = input("Nom : ")
    bio = input("Biographie : ")
    pays = input("Pays d'origine : ")

    info_artiste = {
        "biographie": bio,
        "pays_origine": pays
    }

    sql = f"INSERT INTO Artiste(id, nom, info_artiste) VALUES ({id}, '{nom}', '{json.dumps(info_artiste)}')"
    
    try:
        cursor.execute(sql)
        is_solo = input("Est-ce un artiste solo (oui/non) ? ").strip().lower() == 'oui'
        if is_solo:
            is_in_group = input("Cet artiste solo fait-il partie d'un groupe (oui/non) ? ").strip().lower() == 'oui'
            if is_in_group:
                groupe_id = int(input("Id du groupe : "))
                cursor.execute("INSERT INTO Solo(artisteSolo, groupe) VALUES (%s, %s)", (id, groupe_id))
            else:
                cursor.execute("INSERT INTO Solo(artisteSolo) VALUES (%s)", (id,))
        else:
            cursor.execute("INSERT INTO Groupe(groupe) VALUES (%s)", (id,))
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def display(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Artiste")
        results = cursor.fetchall()
        for x in results:
            print(x)
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def afficher_chansons(conn):
    cursor = conn.cursor()

    val = int(input("Insérer id de l'artiste : "))
    
    # Récupérer les informations de l'artiste
    cursor.execute("SELECT * FROM Artiste WHERE id = %s", (val,))
    artiste = cursor.fetchone()
    
    if not artiste:
        print(f"Aucun artiste trouvé avec l'id {val}")
        return
 
    # Afficher les informations de l'artiste
    print("Informations de l'artiste :")
    print(f"ID: {artiste[0]}")
    print(f"Nom: {artiste[1]}")
    print(f"Biographie: {artiste[2]['biographie']}")
    print(f"Pays d'origine: {artiste[2]['pays_origine']}")

    """ # Vérifier s'il s'agit d'un groupe
    cursor.execute("SELECT * FROM Groupe WHERE groupe = %s", (val,))
    groupe = cursor.fetchone()
    if groupe:
        print("Cet artiste est un groupe.")
    else:
        # Vérifier s'il s'agit d'un artiste solo
        cursor.execute("SELECT * FROM Solo WHERE artisteSolo = %s", (val,))
        solo = cursor.fetchone()
        if solo:
            print("Cet artiste est un artiste solo.")
            if solo[1]:
                print(f"Cet artiste fait partie du groupe avec l'id {solo[1]}")
        else:
            print("Cet artiste n'est ni un groupe ni un artiste solo valide.") """

    try:
        cursor.execute("""
            SELECT c.id, c.titre, TO_CHAR(c.durée, 'HH24:MI:SS'), c.genre
            FROM Chanson c
            WHERE c.auteur = %s
        """, (val,))
        
        results = cursor.fetchall()
        
        if results:
            print(f"Chansons de l'artiste {val}:")
            for row in results:
                print(f"ID: {row[0]}, Titre: {row[1]}, Durée: {row[2]}, Genres: {row[3]}")
        else:
            print(f"Aucune chanson trouvée pour l'artiste {val}.")
    
    except psycopg2.Error as e:
        conn.rollback()
        print("Erreur lors de la récupération des chansons de l'artiste :", e)



def delete(conn):
    cursor = conn.cursor()
    val = int(input("Inserer l'id de l'artiste que vous voulez supprimer : "))
    
    try:
        cursor.execute("DELETE FROM Solo WHERE artisteSolo = %s", (val,))
        cursor.execute("DELETE FROM Groupe WHERE groupe = %s", (val,))
        cursor.execute("DELETE FROM Artiste WHERE id = %s", (val,))
        conn.commit()
        print("Artiste supprimé avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def deleteAll(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Solo")
        cursor.execute("DELETE FROM Groupe")
        cursor.execute("DELETE FROM Artiste")
        conn.commit()
        print("Tous les artistes supprimés avec succès !")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def update(conn):
    cursor = conn.cursor()
    id = int(input("Inserer l'id de l'artiste que vous voulez modifier : "))
    
    cursor.execute("SELECT * FROM Artiste WHERE id = %s", (id,))
    artiste = cursor.fetchone()
    
    if not artiste:
        print(f"Aucun artiste trouvé avec l'id {id}")
        return
 
    nom = artiste[1]
    bio = artiste[2]['biographie']
    po = artiste[2]['pays_origine']


    column_index = int(input("Choisissez la colonne à modifier. Nom : 0, Biographie : 1, Pays d'origine : 2 : "))

 
    if column_index == 0:
        val = input("Nom : ")
        sql = f"UPDATE Artiste SET nom = '{val}' WHERE id = {id}"
    elif column_index == 1:
        val = input("Biographie : ")
        info_artiste = {
        "biographie": val,
        "pays_origine": po
        }
        sql = f"UPDATE Artiste SET info_artiste = '{json.dumps(info_artiste)}' WHERE id = {id}"
    elif column_index == 2:
        val = input("Pays d'origine : ")
        info_artiste = {
        "biographie": bio,
        "pays_origine": val
        }
        sql = f"UPDATE Artiste SET info_artiste = '{json.dumps(info_artiste)}' WHERE id = {id}"

    else:
        print('Colonne invalide !')
        return

    try:
        cursor.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def main(conn):

    i = 0
    while i != 1:
        print("\nQue souhaitez-vous faire ?")
        print("1. Ajouter un artiste")
        print("2. Modifier un artiste")
        print("3. Afficher tous les artistes")
        print("4. Afficher un artiste et ses chansons")
        print("5. Supprimer tous les artistes")
        print("6. Supprimer un artiste")
        print("7. Quitter")
        type = int(input("Saisir le numéro correspondant à votre choix : "))
        
        if type == 1:
            insert(conn)
        elif type == 2:
            update(conn)
        elif type == 3:
            display(conn)
        elif type == 4:
            afficher_chansons(conn)
        elif type == 5:
            deleteAll(conn)
        elif type == 6:
            delete(conn)
        elif type == 7:
            i = 1
        else:
            print("Choix invalide")


