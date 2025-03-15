CREATE TABLE Groupe (
    groupe INT PRIMARY KEY,
    FOREIGN KEY (groupe) REFERENCES Artiste(id)
);