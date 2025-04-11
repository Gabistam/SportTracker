-- Script d'insertion des données pour la table statistiques_joueurs

INSERT INTO statistiques_joueurs (id, joueur_id, match_id, points_marques, minutes_jouees, fautes) VALUES
-- Match 1: Eagles vs Sharks (Basketball)
(1, 1, 1, 15, 28, 2),  -- Dubois (Eagles)
(2, 2, 1, 22, 35, 3),  -- Martin (Eagles)
(3, 3, 1, 10, 20, 1),  -- Petit (Eagles)
(4, 4, 1, 18, 32, 0),  -- Bernard (Eagles)
(5, 5, 1, 13, 25, 4),  -- Robert (Eagles)
(6, 6, 1, 8, 30, 2),   -- Laurent (Sharks)
(7, 7, 1, 12, 33, 2),  -- Leroy (Sharks)
(8, 8, 1, 15, 29, 3),  -- Moreau (Sharks)
(9, 9, 1, 18, 35, 1),  -- Simon (Sharks)
(10, 10, 1, 12, 28, 2), -- Michel (Sharks)

-- Match 2: Lions vs Eagles (Football)
(11, 11, 2, 0, 90, 1),  -- Lefebvre (Lions)
(12, 12, 2, 0, 90, 0),  -- Garcia (Lions)
(13, 13, 2, 1, 85, 2),  -- Roux (Lions)
(14, 14, 2, 0, 90, 1),  -- Fournier (Lions)
(15, 15, 2, 0, 78, 0),  -- Girard (Lions)
(16, 1, 2, 1, 90, 0),   -- Dubois (Eagles)
(17, 2, 2, 1, 75, 1),   -- Martin (Eagles)
(18, 3, 2, 0, 90, 2),   -- Petit (Eagles)
(19, 4, 2, 0, 65, 0),   -- Bernard (Eagles)
(20, 5, 2, 0, 70, 1),   -- Robert (Eagles)

-- Match 3: Sharks vs Lions (Football)
(21, 6, 3, 0, 90, 0),   -- Laurent (Sharks)
(22, 7, 3, 1, 90, 1),   -- Leroy (Sharks)
(23, 8, 3, 2, 85, 0),   -- Moreau (Sharks)
(24, 9, 3, 0, 75, 0),   -- Simon (Sharks)
(25, 10, 3, 0, 90, 2),  -- Michel (Sharks)
(26, 11, 3, 0, 90, 1),  -- Lefebvre (Lions)
(27, 12, 3, 0, 90, 0),  -- Garcia (Lions)
(28, 13, 3, 0, 70, 2),  -- Roux (Lions)
(29, 14, 3, 0, 90, 1),  -- Fournier (Lions)
(30, 15, 3, 0, 82, 0),  -- Girard (Lions)

-- Match 4: Eagles vs Lions (Basketball)
(31, 1, 4, 24, 38, 1),  -- Dubois (Eagles)
(32, 2, 4, 15, 35, 2),  -- Martin (Eagles)
(33, 3, 4, 18, 40, 3),  -- Petit (Eagles)
(34, 4, 4, 12, 30, 1),  -- Bernard (Eagles)
(35, 5, 4, 13, 32, 2),  -- Robert (Eagles)
(36, 11, 4, 22, 37, 3), -- Lefebvre (Lions)
(37, 13, 4, 18, 35, 2), -- Roux (Lions)
(38, 14, 4, 15, 33, 1), -- Fournier (Lions)
(39, 15, 4, 20, 38, 2), -- Girard (Lions)

-- Match 5: Sharks vs Eagles (Football)
(40, 6, 5, 0, 90, 0),   -- Laurent (Sharks)
(41, 7, 5, 0, 90, 1),   -- Leroy (Sharks)
(42, 8, 5, 0, 70, 0),   -- Moreau (Sharks)
(43, 9, 5, 0, 90, 0),   -- Simon (Sharks)
(44, 10, 5, 0, 85, 2),  -- Michel (Sharks)
(45, 1, 5, 1, 90, 0),   -- Dubois (Eagles)
(46, 2, 5, 0, 85, 1),   -- Martin (Eagles)
(47, 3, 5, 1, 90, 0),   -- Petit (Eagles)
(48, 4, 5, 0, 75, 0),   -- Bernard (Eagles)
(49, 5, 5, 0, 65, 0);   -- Robert (Eagles)