# app.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from db_config import DatabaseConnection, test_connection
import models
from views import TeamView, PlayerView, MatchView, RankingView, AddTeamDialog

class SportTrackerApp:
    def __init__(self, root):
        """Initialise l'application SportTracker"""
        self.root = root
        self.root.title("SportTracker Basic")
        self.root.geometry("800x600")
        
        # Vérifier la connexion à la base de données
        if not test_connection():
            messagebox.showerror("Erreur de connexion", 
                                "Impossible de se connecter à PostgreSQL. Vérifiez vos paramètres de connexion.")
            root.destroy()
            return
        
        # Création du menu
        self._create_menu()
        
        # Interface principale avec onglets
        self.notebook = ttk.Notebook(root)
        
        # Onglet Tableau de bord
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Tableau de bord")
        
        # Onglet Équipes
        self.teams_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.teams_tab, text="Équipes")
        
        # Onglet Joueurs
        self.players_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.players_tab, text="Joueurs")
        
        # Onglet Matchs
        self.matches_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.matches_tab, text="Matchs")
        
        # Onglet Classement
        self.ranking_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ranking_tab, text="Classement")
        
        self.notebook.pack(expand=1, fill="both")
        
        # Initialisation des onglets
        self._load_dashboard()
        self._load_teams_tab()
        self._load_matches_tab()
        self._load_ranking_tab()
    
    def _create_menu(self):
        """Crée la barre de menu de l'application"""
        menubar = tk.Menu(self.root)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Actualiser", command=self._refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Menu Équipes
        teams_menu = tk.Menu(menubar, tearoff=0)
        teams_menu.add_command(label="Ajouter une équipe", command=self._show_add_team_dialog)
        menubar.add_cascade(label="Équipes", menu=teams_menu)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="À propos", command=self._show_about_dialog)
        menubar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def _load_dashboard(self):
        """Charge le tableau de bord avec les informations principales"""
        # Nettoyer le tableau de bord
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.dashboard_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Tableau de bord SportTracker", font=("Helvetica", 16))
        title_label.pack(pady=10)
        
        # Statistiques générales
        stats_frame = ttk.LabelFrame(main_frame, text="Statistiques", padding="10")
        stats_frame.pack(fill=tk.X, pady=10)
        
        try:
            # Récupération du nombre d'équipes
            teams = models.get_all_teams()
            team_count = len(teams) if teams else 0
            
            # Récupération du nombre de matchs
            matches = models.get_all_matches()
            match_count = len(matches) if matches else 0
            
            # Affichage des statistiques
            ttk.Label(stats_frame, text=f"Nombre d'équipes: {team_count}").grid(row=0, column=0, padx=20, pady=5, sticky=tk.W)
            ttk.Label(stats_frame, text=f"Nombre total de matchs: {match_count}").grid(row=0, column=1, padx=20, pady=5, sticky=tk.W)
            
            # Prochains matchs et derniers résultats
            if matches:
                # Frame pour les matchs récents
                recent_frame = ttk.LabelFrame(main_frame, text="Derniers résultats", padding="10")
                recent_frame.pack(fill=tk.BOTH, expand=True, pady=10)
                
                # Récupération des 5 derniers matchs
                recent_matches = matches[:5] if len(matches) >= 5 else matches
                
                # Création d'un tableau pour les matchs récents
                columns = ('date', 'match', 'score')
                recent_tree = ttk.Treeview(recent_frame, columns=columns, show='headings', height=5)
                
                recent_tree.heading('date', text='Date')
                recent_tree.heading('match', text='Match')
                recent_tree.heading('score', text='Score')
                
                recent_tree.column('date', width=100)
                recent_tree.column('match', width=300)
                recent_tree.column('score', width=100)
                
                for match in recent_matches:
                    match_id, date, domicile, visiteur, score_dom, score_vis, sport = match
                    match_text = f"{domicile} vs {visiteur} ({sport})"
                    score_text = f"{score_dom or '-'} - {score_vis or '-'}"
                    
                    recent_tree.insert('', tk.END, values=(date, match_text, score_text))
                
                recent_tree.pack(fill=tk.BOTH, expand=True)
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les données: {str(e)}")
    
    def _load_teams_tab(self):
        """Charge l'onglet des équipes"""
        try:
            teams = models.get_all_teams()
            TeamView(self.teams_tab, teams, self._on_team_select)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les équipes: {str(e)}")
    
    def _on_team_select(self, team_id):
        """Gère la sélection d'une équipe dans la liste"""
        if team_id == "refresh":
            self._load_teams_tab()
            return
        
        try:
            # Récupérer les détails de l'équipe
            team = models.get_team_by_id(team_id)
            if not team:
                messagebox.showerror("Erreur", "Équipe non trouvée!")
                return
            
            # Récupérer les joueurs de l'équipe
            players = models.get_players_by_team(team_id)
            
            # Afficher les joueurs dans l'onglet Joueurs
            team_name = team[1]  # Nom de l'équipe
            PlayerView(self.players_tab, players, team_name)
            
            # Basculer sur l'onglet des joueurs
            self.notebook.select(self.players_tab)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les joueurs: {str(e)}")
    
    def _load_matches_tab(self):
        """Charge l'onglet des matchs"""
        try:
            matches = models.get_all_matches()
            MatchView(self.matches_tab, matches)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les matchs: {str(e)}")
    
    def _load_ranking_tab(self):
        """Charge l'onglet du classement"""
        try:
            rankings = models.get_team_ranking()
            RankingView(self.ranking_tab, rankings)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le classement: {str(e)}")
    
    def _refresh_data(self):
        """Actualise toutes les données de l'application"""
        self._load_dashboard()
        self._load_teams_tab()
        self._load_matches_tab()
        self._load_ranking_tab()
        messagebox.showinfo("Actualisation", "Données actualisées avec succès!")
    
    def _show_add_team_dialog(self):
        """Affiche la boîte de dialogue pour ajouter une équipe"""
        AddTeamDialog(self.root, self._add_team)
    
    def _add_team(self, nom, etablissement, coach, division):
        """Ajoute une nouvelle équipe à la base de données"""
        try:
            team_id = models.add_team(nom, etablissement, coach, division)
            if team_id:
                messagebox.showinfo("Succès", f"L'équipe '{nom}' a été ajoutée avec succès!")
                self._load_teams_tab()  # Recharger les équipes
            else:
                messagebox.showerror("Erreur", "Impossible d'ajouter l'équipe!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ajouter l'équipe: {str(e)}")
    
    def _show_about_dialog(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
        SportTracker Basic v1.0
        
        Application de suivi des résultats sportifs
        Développée pour les cours de Master 1
        
        Base de données: PostgreSQL
        Interface: Tkinter
        """
        messagebox.showinfo("À propos", about_text)

# Point d'entrée de l'application
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SportTrackerApp(root)
        root.mainloop()
    finally:
        # Fermer toutes les connexions à la base de données
        DatabaseConnection.close_all_connections()