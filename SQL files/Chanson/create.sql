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
