# models.py
from db_config import execute_query

# Fonctions pour les équipes
def get_all_teams():
    """Récupère toutes les équipes de la base de données"""
    query = """
        SELECT id, nom, etablissement, coach, division 
        FROM equipes 
        ORDER BY nom
    """
    return execute_query(query, fetch=True)

def get_team_by_id(team_id):
    """Récupère une équipe par son ID"""
    query = """
        SELECT id, nom, etablissement, coach, division 
        FROM equipes 
        WHERE id = %s
    """
    result = execute_query(query, (team_id,), fetch=True)
    return result[0] if result else None

def add_team(nom, etablissement, coach, division):
    """Ajoute une nouvelle équipe"""
    query = """
        INSERT INTO equipes (nom, etablissement, coach, division)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """
    result = execute_query(query, (nom, etablissement, coach, division), fetch=True)
    return result[0][0] if result else None

# Fonctions pour les joueurs
def get_players_by_team(team_id):
    """Récupère tous les joueurs d'une équipe"""
    query = """
        SELECT id, nom, prenom, position, annee_naissance 
        FROM joueurs 
        WHERE equipe_id = %s
        ORDER BY nom, prenom
    """
    return execute_query(query, (team_id,), fetch=True)

def add_player(nom, prenom, equipe_id, position, annee_naissance):
    """Ajoute un nouveau joueur"""
    query = """
        INSERT INTO joueurs (nom, prenom, equipe_id, position, annee_naissance)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """
    result = execute_query(
        query, 
        (nom, prenom, equipe_id, position, annee_naissance), 
        fetch=True
    )
    return result[0][0] if result else None

# Fonctions pour les matchs
def get_all_matches():
    """Récupère tous les matchs avec les noms des équipes"""
    query = """
        SELECT m.id, m.date, 
               e1.nom as equipe_domicile, 
               e2.nom as equipe_visiteur, 
               m.score_domicile, 
               m.score_visiteur,
               s.nom as sport
        FROM matchs m
        JOIN equipes e1 ON m.equipe_domicile_id = e1.id
        JOIN equipes e2 ON m.equipe_visiteur_id = e2.id
        JOIN sports s ON m.sport_id = s.id
        ORDER BY m.date DESC
    """
    return execute_query(query, fetch=True)

def add_match(date, equipe_domicile_id, equipe_visiteur_id, score_domicile, score_visiteur, sport_id):
    """Ajoute un nouveau match"""
    query = """
        INSERT INTO matchs (date, equipe_domicile_id, equipe_visiteur_id, score_domicile, score_visiteur, sport_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    result = execute_query(
        query, 
        (date, equipe_domicile_id, equipe_visiteur_id, score_domicile, score_visiteur, sport_id), 
        fetch=True
    )
    return result[0][0] if result else None

# Fonctions pour les sports
def get_all_sports():
    """Récupère tous les sports"""
    query = """
        SELECT id, nom, type, description 
        FROM sports 
        ORDER BY nom
    """
    return execute_query(query, fetch=True)

# Fonctions plus complexes pour les rapports
def get_team_ranking():
    """Récupère le classement des équipes par nombre de victoires"""
    query = """
        WITH victoires AS (
            SELECT equipe_domicile_id as equipe_id, COUNT(*) as nb_victoires
            FROM matchs
            WHERE score_domicile > score_visiteur
            GROUP BY equipe_domicile_id
            UNION ALL
            SELECT equipe_visiteur_id as equipe_id, COUNT(*) as nb_victoires
            FROM matchs
            WHERE score_visiteur > score_domicile
            GROUP BY equipe_visiteur_id
        ),
        total_victoires AS (
            SELECT equipe_id, SUM(nb_victoires) as total
            FROM victoires
            GROUP BY equipe_id
        )
        SELECT e.nom, e.etablissement, COALESCE(t.total, 0) as victoires
        FROM equipes e
        LEFT JOIN total_victoires t ON e.id = t.equipe_id
        ORDER BY victoires DESC
    """
    return execute_query(query, fetch=True)

def get_top_scorers(limit=10):
    """Récupère les meilleurs marqueurs"""
    query = """
        SELECT j.nom, j.prenom, e.nom as equipe, SUM(s.points_marques) as total_points
        FROM statistiques_joueurs s
        JOIN joueurs j ON s.joueur_id = j.id
        JOIN equipes e ON j.equipe_id = e.id
        GROUP BY j.id, e.nom
        ORDER BY total_points DESC
        LIMIT %s
    """
    return execute_query(query, (limit,), fetch=True)

# Si ce fichier est exécuté directement, testons quelques fonctions
if __name__ == "__main__":
    try:
        print("Test des fonctions de modèle:")
        sports = get_all_sports()
        print(f"Nombre de sports: {len(sports)}")
        
        teams = get_all_teams()
        print(f"Nombre d'équipes: {len(teams)}")
        
        if teams:
            team_id = teams[0][0]
            players = get_players_by_team(team_id)
            print(f"L'équipe {teams[0][1]} a {len(players)} joueurs")
        
    except Exception as e:
        print(f"Erreur lors du test des modèles: {e}")