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
