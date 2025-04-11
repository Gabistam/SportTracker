-- Script d'insertion des données pour la table matchs

INSERT INTO matchs (id, date, equipe_domicile_id, equipe_visiteur_id, score_domicile, score_visiteur, sport_id) VALUES
(1, '2023-10-15', 1, 2, 78, 65, 1),  -- Eagles vs Sharks (Basketball)
(2, '2023-10-22', 3, 1, 1, 2, 2),    -- Lions vs Eagles (Football)
(3, '2023-11-05', 2, 3, 3, 0, 2),    -- Sharks vs Lions (Football)
(4, '2023-11-12', 1, 3, 82, 75, 1),  -- Eagles vs Lions (Basketball)
(5, '2023-11-19', 2, 1, 0, 2, 2),    -- Sharks vs Eagles (Football)
(6, '2023-12-03', 4, 5, 95, 87, 1),  -- Tigers vs Bears (Basketball)
(7, '2023-12-10', 6, 7, 3, 1, 2),    -- Panthers vs Wolves (Football)
(8, '2023-12-17', 8, 4, 22, 25, 6),  -- Hawks vs Tigers (Handball)
(9, '2024-01-07', 5, 6, 15, 12, 6),  -- Bears vs Panthers (Handball)
(10, '2024-01-14', 7, 8, 2, 2, 2),   -- Wolves vs Hawks (Football)
(11, '2024-01-21', 9, 10, 0, 3, 2),  -- Dolphins vs Pythons (Football)
(12, '2024-02-04', 10, 1, 68, 72, 1), -- Pythons vs Eagles (Basketball)
(13, '2024-02-11', 2, 9, 4, 0, 2),   -- Sharks vs Dolphins (Football)
(14, '2024-02-18', 3, 7, 28, 24, 6), -- Lions vs Wolves (Handball)
(15, '2024-03-03', 4, 6, 79, 81, 1); -- Tigers vs Panthers (Basketball)