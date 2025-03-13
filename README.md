# Plateforme de Streaming Musical - Base de Données

## Description
Ce projet consiste à concevoir et développer une base de données pour une plateforme de streaming musical avancée. La base de données permet de stocker et gérer les informations relatives aux utilisateurs, artistes, albums, chansons, playlists, historiques d'écoute, genres musicaux et droits d'auteur. En complément, plusieurs requêtes analytiques sont définies pour extraire des informations pertinentes.

## Fonctionnalités
- Gestion des utilisateurs (utilisateurs réguliers et abonnés premium)
- Gestion des artistes (solos, groupes et collaborations)
- Gestion des albums et des chansons
- Création et partage de playlists (publiques, privées, collaboratives)
- Historique d'écoute des utilisateurs
- Analyse des genres préférés des utilisateurs
- Gestion des droits d'auteur

## Structure de la base de données
Le modèle de données inclut les principales entités suivantes :
- **Utilisateur** : Identifiant unique, nom d'utilisateur, adresse mail, mot de passe, date d'inscription, amis, préférences musicales.
- **Artiste** : Identifiant unique, nom d'artiste, biographie, pays d'origine, catalogue de chansons.
- **Album** : Identifiant unique, titre, année de sortie, artiste principal, liste de pistes, durée totale.
- **Chanson** : Identifiant unique, titre, durée, artiste, album, auteurs, compositeurs.
- **Playlist** : Identifiant unique, titre, description, créateur, liste de chansons, permissions d'accès.
- **Historique d'écoute** : Stocke les informations sur les écoutes des utilisateurs.
- **Droits d'auteur** : Enregistre les auteurs, compositeurs et éditeurs des chansons.

## Requêtes demandées
Les requêtes SQL suivantes permettent d'exploiter la base de données :

1. **Durée moyenne des chansons par artiste (si l'artiste a au moins 5 chansons)**
   ```sql
   SELECT artiste.nom, AVG(chanson.duree) AS duree_moyenne
   FROM chanson
   JOIN artiste ON chanson.artiste_id = artiste.id
   GROUP BY artiste.nom
   HAVING COUNT(chanson.id) >= 5;
   ```

2. **Artistes les plus prolifiques (ceux avec le plus de chansons)**
   ```sql
   SELECT artiste.nom, COUNT(chanson.id) AS nombre_chansons
   FROM chanson
   JOIN artiste ON chanson.artiste_id = artiste.id
   GROUP BY artiste.nom
   ORDER BY nombre_chansons DESC;
   ```

3. **Artistes avec les chansons les plus longues (par ex. > 10 minutes)**
   ```sql
   SELECT artiste.nom, chanson.titre, chanson.duree
   FROM chanson
   JOIN artiste ON chanson.artiste_id = artiste.id
   WHERE chanson.duree > 600
   ORDER BY chanson.duree DESC;
   ```

4. **Genres préférés des utilisateurs**
   ```sql
   SELECT utilisateur.nom_utilisateur, genre.nom, COUNT(*) AS nombre_lectures
   FROM historique_ecoute
   JOIN chanson ON historique_ecoute.chanson_id = chanson.id
   JOIN genre ON chanson.genre_id = genre.id
   JOIN utilisateur ON historique_ecoute.utilisateur_id = utilisateur.id
   GROUP BY utilisateur.nom_utilisateur, genre.nom
   ORDER BY utilisateur.nom_utilisateur, nombre_lectures DESC;
   ```

## Technologies utilisées
- **SGBD** : PostgreSQL / MySQL
- **Langage SQL** : Création de la base de données et des requêtes
- **Outils** : SQL Server, MySQL Workbench, pgAdmin

## Auteurs
- Beelayachi Ibrahim
- Camille Milon
- Rayan Feghoul
- Nesrine Serradj


## Remarque
Cette base de données est optimisée pour la gestion efficace des données musicales et propose des analyses avancées pour améliorer l'expérience utilisateur sur la plateforme de streaming.

