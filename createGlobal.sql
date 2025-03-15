CREATE TABLE Album (
    id INT PRIMARY KEY,
    titre VARCHAR NOT NULL,
    annéeSortie INT NOT NULL,
    artistePrincipal INT,
    FOREIGN KEY (artistePrincipal) REFERENCES Artiste(id)
);

CREATE TABLE Artiste (
    id INT PRIMARY KEY,
    nom VARCHAR NOT NULL,
    info_artiste JSON
)

CREATE TABLE ArtisteDroit (
    artiste INT,
    contrat INT,
    PRIMARY KEY (artiste, contrat),
    FOREIGN KEY (artiste) REFERENCES Artiste(id),
    FOREIGN KEY (contrat) REFERENCES DroitAuteur(id)
);

CREATE VIEW ChansonsAuteur AS
SELECT id
FROM Chanson
WHERE id IN (SELECT chanson FROM ArtisteDroit);

ALTER TABLE Chanson ADD CONSTRAINT chanson_auteur CHECK (id IN (SELECT id FROM ChansonsAuteur)); 

CREATE TABLE Chanson (
    id INT PRIMARY KEY,
    titre VARCHAR NOT NULL,
    durée TIME NOT NULL CHECK (durée > '00:00:00'),
    auteur INT,
    album INT,
    FOREIGN KEY (album) REFERENCES Album(id),
    FOREIGN KEY (auteur) REFERENCES artiste(id),
    genre VARCHAR NOT NULL,
);

CREATE TABLE Collaboration (
    album INT,
    artisteInvité INT,
    PRIMARY KEY (album, artisteInvité),
    FOREIGN KEY (album) REFERENCES Album(id),
    FOREIGN KEY (artisteInvité) REFERENCES Artiste(id)
);

CREATE TABLE CompositeurDroit (
    compositeur INT,
    contrat INT,
    PRIMARY KEY (compositeur, contrat),
    FOREIGN KEY (compositeur) REFERENCES Artiste(id),
    FOREIGN KEY (contrat) REFERENCES DroitAuteur(id)
);

CREATE VIEW ChansonsCompositeur AS
SELECT id
FROM Chanson
WHERE id IN (SELECT chanson FROM CompositeurDroit);

ALTER TABLE Chanson
ADD CONSTRAINT chanson_compositeur CHECK (
    (id IN (SELECT id FROM ChansonsCompositeur));


CREATE TABLE DroitAuteur (
    id INT PRIMARY KEY,
    chanson INT UNIQUE NOT NULL,
    editeurs JSON NOT NULL,
    FOREIGN KEY (chanson) REFERENCES Chanson(id),
    CHECK (jsonb_array_length(editeurs) > 0) 
);

CREATE TABLE Groupe (
    groupe INT PRIMARY KEY,
    FOREIGN KEY (groupe) REFERENCES Artiste(id)
);

CREATE TABLE Playlist (
    id INT PRIMARY KEY,
    info_playlist JSON,
    autorisationAcces VARCHAR NOT NULL CHECK (autorisationAcces IN ('privée', 'publique', 'partagée avec des amis')),
    créateur INT,
    chansons JSON,
    albums JSON,
    FOREIGN KEY (créateur) REFERENCES Utilisateur(id)
);
CREATE TABLE Solo (
    artisteSolo INT PRIMARY KEY,
    groupe INT,
    FOREIGN KEY (artisteSolo) REFERENCES Artiste(id),
    FOREIGN KEY (groupe) REFERENCES Groupe(groupe)
);

CREATE VIEW Groupes AS
SELECT id
FROM Artiste
WHERE id IN (SELECT groupe FROM Groupe);

CREATE VIEW Solos AS
SELECT id
FROM Artiste
WHERE id IN (SELECT artisteSolo FROM Solo);

ALTER TABLE Artiste
ADD CONSTRAINT artiste_groupes_solos CHECK (
    (id IN (SELECT id FROM Groupes) AND id NOT IN (SELECT id FROM Solos))
    OR
    (id IN (SELECT id FROM Solos) AND id NOT IN (SELECT id FROM Groupes))
);


CREATE TABLE Utilisateur (
    id INT PRIMARY KEY,
    nom VARCHAR NOT NULL,
    mail VARCHAR NOT NULL UNIQUE,
    mdp VARCHAR NOT NULL,
    dateInscription DATE NOT NULL,
    type VARCHAR NOT NULL CHECK (type IN ('Régulier', 'Premium')),
    preferences JSON,
    amis JSON
);