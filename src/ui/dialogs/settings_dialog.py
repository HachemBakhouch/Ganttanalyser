import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any


class AnalysisSettingsDialog(tk.Toplevel):
    """
    Boîte de dialogue pour configurer les paramètres avancés de l'analyse comparative
    """

    def __init__(self, parent: tk.Tk):
        """
        Initialise la boîte de dialogue de paramètres

        :param parent: Fenêtre parente
        """
        super().__init__(parent)

        self.title("Paramètres d'analyse comparative")
        self.geometry("500x600")
        self.resizable(False, False)

        # Variable pour stocker les paramètres
        self._settings = {}

        # Créer les widgets
        self._create_widgets()

    def _create_widgets(self):
        """
        Crée les widgets de la boîte de dialogue
        """
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Section Comparaison
        comparison_frame = ttk.LabelFrame(main_frame, text="Paramètres de Comparaison")
        comparison_frame.pack(fill=tk.X, pady=(0, 10))

        # Seuils de détection de changement
        ttk.Label(comparison_frame, text="Seuils de détection de changement:").pack(
            anchor=tk.W
        )

        # Seuil de changement de charge de travail (%)
        workload_frame = ttk.Frame(comparison_frame)
        workload_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(workload_frame, text="Variation de charge de travail (%)").pack(
            side=tk.LEFT
        )
        self.workload_threshold = ttk.Entry(workload_frame, width=10)
        self.workload_threshold.pack(side=tk.RIGHT)
        self.workload_threshold.insert(0, "10")  # Valeur par défaut 10%

        # Seuil de nouveaux projets
        new_project_frame = ttk.Frame(comparison_frame)
        new_project_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(new_project_frame, text="Nouveaux projets (nombre minimum)").pack(
            side=tk.LEFT
        )
        self.new_project_threshold = ttk.Entry(new_project_frame, width=10)
        self.new_project_threshold.pack(side=tk.RIGHT)
        self.new_project_threshold.insert(
            0, "2"
        )  # Valeur par défaut 2 nouveaux projets

        # Section Profils
        profiles_frame = ttk.LabelFrame(main_frame, text="Configuration des Profils")
        profiles_frame.pack(fill=tk.X, pady=(10, 10))

        # Profils prioritaires
        ttk.Label(
            profiles_frame, text="Profils prioritaires (séparés par des virgules)"
        ).pack(anchor=tk.W)
        self.priority_profiles = ttk.Entry(profiles_frame, width=50)
        self.priority_profiles.pack(fill=tk.X, pady=(5, 0))

        # Fenêtre de comparaison temporelle
        timeframe_frame = ttk.LabelFrame(main_frame, text="Fenêtre de Comparaison")
        timeframe_frame.pack(fill=tk.X, pady=(0, 10))

        # Nombre de semaines à comparer
        weeks_frame = ttk.Frame(timeframe_frame)
        weeks_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(weeks_frame, text="Nombre de semaines à comparer").pack(side=tk.LEFT)
        self.weeks_to_compare = ttk.Entry(weeks_frame, width=10)
        self.weeks_to_compare.pack(side=tk.RIGHT)
        self.weeks_to_compare.insert(0, "4")  # Comparer sur 4 semaines par défaut

        # Options avancées
        advanced_frame = ttk.LabelFrame(main_frame, text="Options Avancées")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))

        # Ignorer certains types de projets
        ttk.Label(
            advanced_frame, text="Types de projets à ignorer (séparés par des virgules)"
        ).pack(anchor=tk.W)
        self.ignored_project_types = ttk.Entry(advanced_frame, width=50)
        self.ignored_project_types.pack(fill=tk.X, pady=(5, 0))

        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(
            side=tk.RIGHT, padx=5
        )
        ttk.Button(button_frame, text="Annuler", command=self.destroy).pack(
            side=tk.RIGHT
        )

    def _on_ok(self):
        """
        Valide et sauvegarde les paramètres
        """
        try:
            # Valider et convertir les entrées
            self._settings = {
                "workload_threshold": float(self.workload_threshold.get()),
                "new_project_threshold": int(self.new_project_threshold.get()),
                "priority_profiles": [
                    p.strip()
                    for p in self.priority_profiles.get().split(",")
                    if p.strip()
                ],
                "weeks_to_compare": int(self.weeks_to_compare.get()),
                "ignored_project_types": [
                    p.strip()
                    for p in self.ignored_project_types.get().split(",")
                    if p.strip()
                ],
            }

            # Fermer la boîte de dialogue
            self.destroy()

        except ValueError as e:
            messagebox.showerror(
                "Erreur de saisie", f"Veuillez vérifier vos saisies : {str(e)}"
            )

    def show(self) -> Optional[Dict[str, Any]]:
        """
        Affiche la boîte de dialogue et attend la sélection

        :return: Dictionnaire de paramètres ou None si annulé
        """
        # Attendre que la boîte de dialogue soit fermée
        self.wait_window(self)

        return self._settings if self._settings else None
