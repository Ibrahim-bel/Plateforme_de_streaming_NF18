CREATE TABLE Album (
    id INT PRIMARY KEY,
    titre VARCHAR NOT NULL,
    annéeSortie INT NOT NULL,
    artistePrincipal INT,
    FOREIGN KEY (artistePrincipal) REFERENCES Artiste(id)
);
