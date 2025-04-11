# db_config.py
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class DatabaseConnection:
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls, config=None):
        """Initialise le pool de connexions à PostgreSQL"""
        if config is None:
            # Configuration par défaut utilisant les variables d'environnement
            config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'database': os.getenv('DB_NAME', 'sporttracker'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', ''),
                'port': os.getenv('DB_PORT', '5432')
            }
        
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,  # Nombre minimal de connexions
                10, # Nombre maximal de connexions
                **config
            )
            print("✓ Pool de connexions créé avec succès")
        except (Exception, psycopg2.Error) as error:
            print(f"✗ Erreur lors de la connexion à PostgreSQL: {error}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Obtient une connexion depuis le pool"""
        if cls._connection_pool is None:
            cls.initialize_pool()
        return cls._connection_pool.getconn()
    
    @classmethod
    def release_connection(cls, connection):
        """Libère une connexion et la retourne au pool"""
        cls._connection_pool.putconn(connection)
    
    @classmethod
    def close_all_connections(cls):
        """Ferme toutes les connexions dans le pool"""
        if cls._connection_pool:
            cls._connection_pool.closeall()


# Fonction utilitaire pour exécuter des requêtes
def execute_query(query, params=None, fetch=False):
    """
    Exécute une requête SQL et renvoie éventuellement des résultats
    
    Args:
        query (str): Requête SQL à exécuter
        params (tuple, optional): Paramètres pour la requête
        fetch (bool, optional): Si True, récupère et renvoie les résultats
    
    Returns:
        list ou None: Résultats de la requête si fetch=True, sinon None
    """
    connection = None
    results = None
    
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            results = cursor.fetchall()
        else:
            connection.commit()
            
        cursor.close()
        
    except (Exception, psycopg2.Error) as error:
        if connection:
            connection.rollback()
        print(f"✗ Erreur lors de l'exécution de la requête: {error}")
        raise
    
    finally:
        if connection:
            DatabaseConnection.release_connection(connection)
    
    return results


# Fonction pour tester la connexion
def test_connection():
    """Teste la connexion à la base de données"""
    try:
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        cursor.close()
        
        print(f"✓ Connexion à PostgreSQL réussie!")
        print(f"✓ Version de PostgreSQL: {db_version[0]}")
        
        DatabaseConnection.release_connection(connection)
        return True
    
    except (Exception, psycopg2.Error) as error:
        print(f"✗ Erreur lors du test de connexion à PostgreSQL: {error}")
        return False


# Si ce fichier est exécuté directement, testons la connexion
if __name__ == "__main__":
    test_connection()