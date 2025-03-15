import psycopg2
import requete
import album
import utilisateur
import playlist
import artiste
import chanson
import collaboration

HOST = "tuxa.sme.utc"
USER = "nf18p097"
PASSWORD = "1lqi2PAuj9UX"
DATABASE = "dbnf18p097"

def main():
    try:
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" %(HOST,DATABASE, USER, PASSWORD))
        print("connexion reussie")

        i = 0
        while i != 1 :

            choix = int(input("Tapez 0 pour manipuler les données ou 1 pour lancer les requêtes. "))

            if choix == 0 :
                print("1 : Utilisateur")
                print("2 : Artiste")
                #print("3 : Album")
                #print("4 : Collaboration d'un album")
                #print("5 : Chanson")
                #print("6 : Playlist")
                table_index = int(input("Entrez votre choix : "))

                if table_index == 1:
                    utilisateur.main(conn)
                elif table_index == 2:
                    artiste.main(conn)
                '''elif table_index == 3:
                    album.main(conn)
                elif table_index == 4:
                    collaboration.main(conn)
                elif table_index == 5:
                    chanson.main(conn)
                elif table_index == 6:
                    playlist.main(conn)'''
               
            elif choix == 1:
                requete.main(conn)

            else:
                print('Commande incorrecte!')
                print()

            i = int(input("Tapez 1 pour sortir, sinon 0 pour continuer : "))
            print()
        conn.close()
    except Exception as error:
        print("Une exception  s'est produite: ", error)
        print()
        print("Type d'exception: ", type(error))
        print()

    return

main()