# views.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class TeamView:
    def __init__(self, parent_frame, teams, on_team_select=None):
        """
        Crée une vue pour afficher les équipes
        
        Args:
            parent_frame: Le cadre parent Tkinter
            teams: Liste des équipes à afficher
            on_team_select: Fonction à appeler lorsqu'une équipe est sélectionnée
        """
        self.parent = parent_frame
        self.on_team_select = on_team_select
        
        # Nettoyer le cadre
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Frame pour les options
        options_frame = ttk.Frame(parent_frame)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="Équipes").pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame, text="Actualiser", 
                   command=lambda: self.on_team_select("refresh")).pack(side=tk.RIGHT)
        
        # Frame pour le tableau
        table_frame = ttk.Frame(parent_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Créer le tableau
        columns = ('id', 'nom', 'etablissement', 'coach', 'division')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Définir les en-têtes
        self.tree.heading('id', text='ID')
        self.tree.heading('nom', text='Nom')
        self.tree.heading('etablissement', text='Établissement')
        self.tree.heading('coach', text='Coach')
        self.tree.heading('division', text='Division')
        
        # Ajuster les colonnes
        self.tree.column('id', width=50)
        self.tree.column('nom', width=150)
        self.tree.column('etablissement', width=200)
        self.tree.column('coach', width=150)
        self.tree.column('division', width=100)
        
        # Insérer les données
        for team in teams:
            self.tree.insert('', tk.END, values=team)
        
        # Ajouter un événement de sélection
        if on_team_select:
            self.tree.bind('<<TreeviewSelect>>', self._on_team_selected)
        
        # Ajouter des barres de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Placer les éléments
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _on_team_selected(self, event):
        """Gère l'événement de sélection d'une équipe"""
        if self.on_team_select:
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                team_id = item['values'][0]  # Premier élément: ID
                self.on_team_select(team_id)


class PlayerView:
    def __init__(self, parent_frame, players, team_name=None):
        """
        Crée une vue pour afficher les joueurs
        
        Args:
            parent_frame: Le cadre parent Tkinter
            players: Liste des joueurs à afficher
            team_name: Nom de l'équipe des joueurs (facultatif)
        """
        # Nettoyer le cadre
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Frame pour les options
        options_frame = ttk.Frame(parent_frame)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        if team_name:
            ttk.Label(options_frame, text=f"Joueurs de l'équipe {team_name}").pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(options_frame, text="Tous les joueurs").pack(side=tk.LEFT, padx=5)
        
        # Frame pour le tableau
        table_frame = ttk.Frame(parent_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Créer le tableau
        columns = ('id', 'nom', 'prenom', 'position', 'annee')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Définir les en-têtes
        self.tree.heading('id', text='ID')
        self.tree.heading('nom', text='Nom')
        self.tree.heading('prenom', text='Prénom')
        self.tree.heading('position', text='Position')
        self.tree.heading('annee', text='Année naissance')
        
        # Ajuster les colonnes
        self.tree.column('id', width=50)
        self.tree.column('nom', width=150)
        self.tree.column('prenom', width=150)
        self.tree.column('position', width=100)
        self.tree.column('annee', width=100)
        
        # Insérer les données
        for player in players:
            self.tree.insert('', tk.END, values=player)
        
        # Ajouter des barres de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Placer les éléments
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


class MatchView:
    def __init__(self, parent_frame, matches):
        """
        Crée une vue pour afficher les matchs
        
        Args:
            parent_frame: Le cadre parent Tkinter
            matches: Liste des matchs à afficher
        """
        # Nettoyer le cadre
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Frame pour les options
        options_frame = ttk.Frame(parent_frame)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="Matchs récents").pack(side=tk.LEFT, padx=5)
        
        # Frame pour le tableau
        table_frame = ttk.Frame(parent_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Créer le tableau
        columns = ('id', 'date', 'domicile', 'visiteur', 'score', 'sport')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Définir les en-têtes
        self.tree.heading('id', text='ID')
        self.tree.heading('date', text='Date')
        self.tree.heading('domicile', text='Équipe domicile')
        self.tree.heading('visiteur', text='Équipe visiteur')
        self.tree.heading('score', text='Score')
        self.tree.heading('sport', text='Sport')
        
        # Ajuster les colonnes
        self.tree.column('id', width=50)
        self.tree.column('date', width=100)
        self.tree.column('domicile', width=150)
        self.tree.column('visiteur', width=150)
        self.tree.column('score', width=100)
        self.tree.column('sport', width=100)
        
        # Insérer les données
        for match in matches:
            match_id, date, domicile, visiteur, score_dom, score_vis, sport = match
            score_txt = f"{score_dom or '-'} - {score_vis or '-'}"
            self.tree.insert('', tk.END, values=(match_id, date, domicile, visiteur, score_txt, sport))
        
        # Ajouter des barres de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Placer les éléments
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


class RankingView:
    def __init__(self, parent_frame, rankings):
        """
        Crée une vue pour afficher le classement des équipes
        
        Args:
            parent_frame: Le cadre parent Tkinter
            rankings: Liste des équipes avec leur nombre de victoires
        """
        # Nettoyer le cadre
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Frame pour les options
        options_frame = ttk.Frame(parent_frame)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="Classement des équipes").pack(side=tk.LEFT, padx=5)
        
        # Frame pour le tableau
        table_frame = ttk.Frame(parent_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Créer le tableau
        columns = ('rang', 'equipe', 'etablissement', 'victoires')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Définir les en-têtes
        self.tree.heading('rang', text='#')
        self.tree.heading('equipe', text='Équipe')
        self.tree.heading('etablissement', text='Établissement')
        self.tree.heading('victoires', text='Victoires')
        
        # Ajuster les colonnes
        self.tree.column('rang', width=50)
        self.tree.column('equipe', width=150)
        self.tree.column('etablissement', width=200)
        self.tree.column('victoires', width=100)
        
        # Insérer les données
        for i, (nom, etablissement, victoires) in enumerate(rankings, 1):
            self.tree.insert('', tk.END, values=(i, nom, etablissement, victoires))
        
        # Ajouter des barres de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Placer les éléments
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


class AddTeamDialog:
    def __init__(self, parent, callback):
        """
        Crée une boîte de dialogue pour ajouter une équipe
        
        Args:
            parent: La fenêtre parente
            callback: Fonction à appeler avec les données de la nouvelle équipe
        """
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Ajouter une équipe")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Champs du formulaire
        ttk.Label(self.dialog, text="Nom de l'équipe:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.nom_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.nom_var, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="Établissement:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.etablissement_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.etablissement_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="Coach:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.coach_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.coach_var, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(self.dialog, text="Division:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.division_var = tk.StringVar()
        ttk.Combobox(self.dialog, textvariable=self.division_var, values=["Division 1", "Division 2", "Division 3"]).grid(row=3, column=1, padx=10, pady=5)
        
        # Boutons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Annuler", command=self.dialog.destroy).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Ajouter", command=self._on_submit).pack(side=tk.LEFT)
    
    def _on_submit(self):
        """Valide et envoie les données du formulaire"""
        nom = self.nom_var.get().strip()
        etablissement = self.etablissement_var.get().strip()
        coach = self.coach_var.get().strip()
        division = self.division_var.get()
        
        if not nom or not etablissement:
            messagebox.showerror("Erreur", "Le nom de l'équipe et l'établissement sont obligatoires!")
            return
        
        self.callback(nom, etablissement, coach, division)
        self.dialog.destroy()


# Si ce fichier est exécuté directement, testons une interface simple
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test des vues")
    root.geometry("800x600")
    
    # Simulons quelques données
    teams = [
        (1, "Eagles", "Université Paris-Sud", "Jean Dupont", "Division 1"),
        (2, "Sharks", "École Polytechnique", "Marie Martin", "Division 1"),
        (3, "Lions", "Université Lyon 3", "Pierre Durant", "Division 2")
    ]
    
    players = [
        (1, "Dubois", "Thomas", "Meneur", 2002),
        (2, "Martin", "Julie", "Ailier", 2003),
        (3, "Bernard", "Lucas", "Gardien", 2001)
    ]
    
    matches = [
        (1, "2023-10-15", "Eagles", "Sharks", 78, 65, "Basketball"),
        (2, "2023-10-22", "Lions", "Eagles", 1, 2, "Football"),
        (3, "2023-11-05", "Sharks", "Lions", 3, 0, "Football")
    ]
    
    # Créons un notebook pour tester les différentes vues
    notebook = ttk.Notebook(root)
    
    teams_tab = ttk.Frame(notebook)
    players_tab = ttk.Frame(notebook)
    matches_tab = ttk.Frame(notebook)
    
    notebook.add(teams_tab, text="Équipes")
    notebook.add(players_tab, text="Joueurs")
    notebook.add(matches_tab, text="Matchs")
    
    notebook.pack(expand=1, fill="both")
    
    # Affichons nos vues
    TeamView(teams_tab, teams)
    PlayerView(players_tab, players)
    MatchView(matches_tab, matches)
    
    root.mainloop()