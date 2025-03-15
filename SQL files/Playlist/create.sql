CREATE TABLE Playlist (
    id INT PRIMARY KEY,
    info_playlist JSON,
    autorisationAcces VARCHAR NOT NULL CHECK (autorisationAcces IN ('privée', 'publique', 'partagée avec des amis')),
    créateur INT,
    chansons JSON,
    albums JSON,
    FOREIGN KEY (créateur) REFERENCES Utilisateur(id)
);
