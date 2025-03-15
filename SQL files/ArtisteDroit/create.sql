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
