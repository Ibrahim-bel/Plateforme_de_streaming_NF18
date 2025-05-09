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