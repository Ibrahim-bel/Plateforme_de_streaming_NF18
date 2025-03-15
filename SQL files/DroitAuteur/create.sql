CREATE TABLE DroitAuteur (
    id INT PRIMARY KEY,
    chanson INT UNIQUE NOT NULL,
    editeurs JSON NOT NULL,
    FOREIGN KEY (chanson) REFERENCES Chanson(id),
    CHECK (jsonb_array_length(editeurs) > 0) 
);