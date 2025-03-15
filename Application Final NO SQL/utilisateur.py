#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
#print("test")

def insert(conn):
    cursor = conn.cursor()
    id = int(input("Id : "))
    nom = input("Nom : ")
    mail = input("Adresse mail : ")
    mdp = input("Mot de passe : ")
    dateInscription = input("Date d'inscription (YYYY-MM-DD): ")
    type_abonnee = input("Type d'abonnement : ")
    preferences = input('Preferences (si plusieurs préférences, entrez au format suivant "...","...",...) : ')
    amis = input('Amis (si plusieurs amis, entrez au format suivant ..., ..., ...) : ')

    sql = f"INSERT INTO Utilisateur(id, nom, mail, mdp, dateInscription, type, preferences, amis) VALUES ({id}, '{nom}', '{mail}', '{mdp}', '{dateInscription}', '{type_abonnee}', '[{preferences}]', '[{amis}]')"

    try :
        cursor.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def display(conn):
    cursor = conn.cursor()
    try :
        cursor.execute("SELECT id, nom, mail, TO_CHAR(dateInscription, 'DD/MM/YY'), type, preferences, amis FROM Utilisateur")
        results = cursor.fetchall()
        for x in results:
            print(x)

    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)
        
def display_amis(conn):
    cursor = conn.cursor()
    val = int(input("Inserer l'id de l'utilisateur dont vous voulez afficher les amis : "))
    try :
        cursor.execute(f"SELECT u.id, a.* FROM Utilisateur u, JSON_ARRAY_ELEMENTS(u.amis) a WHERE id = {val}")
        results = cursor.fetchall()
        for x in results:
            print(x)

    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)   
        
def display_preferences(conn):
    cursor = conn.cursor()
    val = int(input("Inserer l'id de l'utilisateur dont vous voulez afficher les préférences : "))
    try :
        cursor.execute(f"SELECT preferences FROM Utilisateur WHERE id = {val}")
        results = cursor.fetchall()
        for x in results:
            print(x)

    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)  

def delete(conn):
    cursor = conn.cursor()
    val = int(input("Inserer l'id de l'utilisateur que vous voulez supprimer : "))
    sql = f"DELETE FROM Utilisateur WHERE id = {val}"
    try :
        cursor.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)


def deleteAll(conn):
    cursor = conn.cursor()
    sql = "DELETE FROM Utilisateur"
    try :
        cursor.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)


def update(conn):
    cursor = conn.cursor()
    id = int(input("Inserer l'id de l'utilisateur que vous voulez modifier : "))
    column_index = int(input("Choisissez la column à modifier. Mail : 0, Mot de passe : 1, Type d'abonnement : 2, Nom : 3  "))

    if column_index == 0:
        val = input("Quelles donnée voulez vous insérer en remplacement? ")
        sql = f"UPDATE Utilisateur SET mail = '{val}' WHERE id = {id}"
    elif column_index == 1:
        val = input("Quelles donnée voulez vous insérer en remplacement?")
        sql = f"UPDATE Utilisateur SET mdp = '{val}' WHERE id = {id}"
    elif column_index == 2:
        val = input("Quelles donnée voulez vous insérer en remplacement?")
        sql = f"UPDATE Utilisateur SET type = '{val}' WHERE id = {id}"
    elif column_index == 3:
        val = input("Quelles donnée voulez vous insérer en remplacement?")
        sql = f"UPDATE Utilisateur SET nom = '{val}' WHERE id = {id}"
    else:
        print('Colonne invalide !')
        return

    try :
        cursor.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def update_user_friends(conn, user_id, action, friend_id=None, new_friend_id=None):
    cursor = conn.cursor()
    cursor.execute(f"SELECT amis FROM Utilisateur WHERE id = {user_id}")
    result = cursor.fetchone()
    
    if result is None:
        print("Utilisateur non trouvé.")
        return

    friends_list = result[0]

    if action == 0:
        if friend_id is not None and friend_id not in friends_list:
            friends_list.append(friend_id)
    elif action == 1:
        if friend_id in friends_list and new_friend_id is not None:
            friends_list[friends_list.index(friend_id)] = new_friend_id
    elif action == 2:  # Retirer un ami
        if friend_id in friends_list:
            friends_list.remove(friend_id)
    else:
        print("Action non valide.")
        return
    try :
        cursor.execute(f"UPDATE Utilisateur SET amis = '{friends_list}' WHERE id = {user_id}")
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)

def update_user_preferences(conn, user_id, action, preference=None, new_preference=None):
    cursor = conn.cursor()
    cursor.execute(f"SELECT preferences FROM Utilisateur WHERE id = {user_id}")
    result = cursor.fetchone()
    if result is None:
        print("Utilisateur non trouvé.")
        return
    
    

    preferences_list = result[0]
    if action == 0:  # Ajouter une préférence
        if preference is not None and preference not in preferences_list:
            preferences_list.append(preference)
    elif action == 1:  # Modifier une préférence
        if preference in preferences_list and new_preference is not None:
            preferences_list[preferences_list.index(preference)] = new_preference
    elif action == 2:  # Retirer une préférence
        if preference in preferences_list:
            preferences_list.remove(preference)
    else:
        print("Action non valide.")
        return
    try :
        liste_chaine = str(preferences_list)
        print(liste_chaine)
        liste_chaine_modifiee = liste_chaine.replace("'", '"')
        cursor.execute(f"UPDATE Utilisateur SET preferences = '{liste_chaine_modifiee}' WHERE id = {user_id}")
        conn.commit()
    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("Message système :", e)


def main(conn):

    i = 0
    while i != 1:
        print("\nQue souhaitez-vous faire ?")
        print("1. Ajouter un utilisateur")
        print("2. Modifier un utilisateur")
        print("3. Afficher tous les utilisateurs")
        print("4. Supprimer tous les utilisateurs")
        print("5. Supprimer un utilisateur")
        print("6. Gérer les amis d'un utilisateur")
        print("7. Gérer les préférences d'un utilisateur")
        print("8. Quitter")
        type = int(input("Saisir le numéro correspondant à votre choix : "))

        if type == 1:
            insert(conn)
        elif type == 2:
            update(conn)
        elif type == 3:
            display(conn)
        elif type == 4:
            deleteAll(conn)
        elif type == 5:
            delete(conn)
        elif type == 6:
            j = 0
            while j != 1:
                print("\nQue souhaitez-vous faire ?")
                print("1. Ajouter un ami")
                print("2. Modifier un ami")
                print("3. Supprimer un ami")
                print("4. Afficher les amis d'un utilisateur")
                print("5. Quitter")
                type = int(input("Saisir le numéro correspondant à votre choix : "))

                if type == 1:
                    id = int(input("Inserer l'id de l'utilisateur : "))
                    friend_id = int(input("Inserer l'id de l'ami à ajouter : "))
                    update_user_friends(conn,id,0,friend_id)

                elif type == 2:
                    id = int(input("Inserer l'id de l'utilisateur : "))
                    friend_id = int(input("Inserer l'id de l'ami à modifier : "))
                    new_friend_id = int(input("Inserer l'id du nouvel id de l'ami : "))
                    update_user_friends(conn,id,1,friend_id, new_friend_id)
                elif type == 3:
                    id = int(input("Inserer l'id de l'utilisateur : "))
                    friend_id = int(input("Inserer l'id de l'ami à retirer : "))
                    update_user_friends(conn,id,2,friend_id)
                elif type == 4:
                    display_amis(conn)
                elif type == 5:
                    j = 1
        elif type == 7:
            j = 0
            while j != 1:
                print("\nQue souhaitez-vous faire ?")
                print("1. Ajouter une préférence")
                print("2. Modifier une préférence")
                print("3. Supprimer une préférence")
                print("4. Afficher les préférencces d'un utilisateur")
                print("5. Quitter")
                type = int(input("Saisir le numéro correspondant à votre choix : "))
                
                if type == 1:
                    id = int(input("Inserer l'id de l'utilisateur : "))
                    preference = input("Inserer la préférence à ajouter : ")
                    update_user_preferences(conn,id,0,preference)
                elif type == 2:
                    id = int(input("Inserer l'id de l'utilisateur : "))
                    preference = input("Inserer la préférence à modifier : ")
                    new_preference = input("Inserer la nouvelle préférence : ")
                    update_user_preferences(conn,id,1,preference, new_preference)
                elif type == 3:
                    id = int(input("Inserer l'id de l'utilisateur : "))
                    preference = input("Inserer la préférence à retirer : ")
                    update_user_preferences(conn,id,2,preference)
                elif type == 4:
                    display_preferences(conn)
                elif type == 5:
                    j = 1
        elif type == 8:
            i = 1
        else:
            print("Choix invalide")

    return


