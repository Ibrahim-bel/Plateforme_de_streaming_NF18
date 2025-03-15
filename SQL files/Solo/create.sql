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