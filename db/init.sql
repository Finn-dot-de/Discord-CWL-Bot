-- Erstelle die Tabelle 'cwl'
CREATE TABLE IF NOT EXISTS cwl (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    townhall INTEGER NOT NULL
);

-- -- Optional: Füge einige Anfangsdaten hinzu
-- INSERT INTO cwl (username, townhall) VALUES
-- ('Benutzer1', 5),
-- ('Benutzer2', 3);
