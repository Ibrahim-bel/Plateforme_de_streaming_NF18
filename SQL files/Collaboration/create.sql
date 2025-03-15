CREATE TABLE Collaboration (
    album INT,
    artisteInvité INT,
    PRIMARY KEY (album, artisteInvité),
    FOREIGN KEY (album) REFERENCES Album(id),
    FOREIGN KEY (artisteInvité) REFERENCES Artiste(id)
);