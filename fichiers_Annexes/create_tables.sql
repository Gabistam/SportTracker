-- Script de création des tables pour SportTracker Basic

-- Suppression des tables si elles existent déjà (pour réinitialisation)
DROP TABLE IF EXISTS statistiques_joueurs CASCADE;
DROP TABLE IF EXISTS matchs CASCADE;
DROP TABLE IF EXISTS joueurs CASCADE;
DROP TABLE IF EXISTS equipes CASCADE;
DROP TABLE IF EXISTS sports CASCADE;

-- Table des sports
CREATE TABLE sports (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('Équipe', 'Individuel')),
    description TEXT
);

-- Table des équipes
CREATE TABLE equipes (
    id INTEGER PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    etablissement VARCHAR(200) NOT NULL,
    coach VARCHAR(100),
    division VARCHAR(50) CHECK (division IN ('Division 1', 'Division 2', 'Division 3'))
);

-- Table des joueurs
CREATE TABLE joueurs (
    id INTEGER PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    equipe_id INTEGER REFERENCES equipes(id) ON DELETE SET NULL,
    position VARCHAR(50),
    annee_naissance INTEGER CHECK (annee_naissance BETWEEN 1950 AND 2010)
);

-- Table des matchs
CREATE TABLE matchs (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    equipe_domicile_id INTEGER REFERENCES equipes(id) ON DELETE CASCADE,
    equipe_visiteur_id INTEGER REFERENCES equipes(id) ON DELETE CASCADE,
    score_domicile INTEGER CHECK (score_domicile >= 0 OR score_domicile IS NULL),
    score_visiteur INTEGER CHECK (score_visiteur >= 0 OR score_visiteur IS NULL),
    sport_id INTEGER REFERENCES sports(id) ON DELETE CASCADE,
    -- Contrainte: l'équipe domicile et visiteur doivent être différentes
    CONSTRAINT different_teams CHECK (equipe_domicile_id != equipe_visiteur_id)
);

-- Table des statistiques des joueurs
CREATE TABLE statistiques_joueurs (
    id SERIAL PRIMARY KEY,
    joueur_id INTEGER REFERENCES joueurs(id) ON DELETE CASCADE,
    match_id INTEGER REFERENCES matchs(id) ON DELETE CASCADE,
    points_marques INTEGER DEFAULT 0,
    minutes_jouees INTEGER DEFAULT 0 CHECK (minutes_jouees >= 0),
    fautes INTEGER DEFAULT 0 CHECK (fautes >= 0),
    CONSTRAINT unique_joueur_match UNIQUE (joueur_id, match_id)
);

-- Création d'index pour améliorer les performances
CREATE INDEX idx_joueurs_equipe ON joueurs(equipe_id);
CREATE INDEX idx_matchs_equipe_domicile ON matchs(equipe_domicile_id);
CREATE INDEX idx_matchs_equipe_visiteur ON matchs(equipe_visiteur_id);
CREATE INDEX idx_matchs_sport ON matchs(sport_id);
CREATE INDEX idx_statistiques_joueur ON statistiques_joueurs(joueur_id);
CREATE INDEX idx_statistiques_match ON statistiques_joueurs(match_id);