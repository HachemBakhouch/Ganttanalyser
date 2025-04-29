import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Tuple, Any

from src.data.data_models import ProfileWorkload, WorkloadEntry


class ResultsDisplay(ttk.Frame):
    """
    Composant pour afficher les résultats de l'analyse de charge de travail
    """

    def __init__(self, master: tk.Tk):
        """
        Initialise l'affichage des résultats

        :param master: Widget parent
        """
        super().__init__(master)

        # Variables pour stocker les résultats
        self._profiles_workload: List[ProfileWorkload] = []
        self._detailed_workload: Dict[str, Dict[str, List[WorkloadEntry]]] = {}

        # Créer les widgets
        self._create_widgets()

    def _create_widgets(self):
        """
        Crée les widgets pour l'affichage des résultats
        """
        # Frame principal avec onglets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Onglet des résultats globaux
        self.global_results_text = tk.Text(
            self.notebook, wrap=tk.WORD, height=15, state=tk.DISABLED
        )
        self.global_results_text.pack(fill=tk.BOTH, expand=True)

        # Onglet des résultats détaillés
        self.detailed_results_text = tk.Text(
            self.notebook, wrap=tk.WORD, height=15, state=tk.DISABLED
        )
        self.detailed_results_text.pack(fill=tk.BOTH, expand=True)

        # Ajouter les onglets
        self.notebook.add(self.global_results_text, text="Résultats Globaux")
        self.notebook.add(self.detailed_results_text, text="Résultats Détaillés")

    def display_results(
        self,
        profiles_workload: List[ProfileWorkload],
        detailed_workload: Dict[str, Dict[str, List[WorkloadEntry]]],
    ):
        """
        Affiche les résultats de l'analyse

        :param profiles_workload: Charge de travail globale par profil
        :param detailed_workload: Charge de travail détaillée
        """
        # Stocker les résultats
        self._profiles_workload = profiles_workload
        self._detailed_workload = detailed_workload

        # Effacer les résultats précédents
        self._clear_results()

        # Afficher les résultats globaux
        self._display_global_results(profiles_workload)

        # Afficher les résultats détaillés
        self._display_detailed_results(detailed_workload)

    def _clear_results(self):
        """
        Efface les résultats actuels
        """
        for text_widget in [self.global_results_text, self.detailed_results_text]:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.config(state=tk.DISABLED)

    def _display_global_results(self, profiles_workload: List[ProfileWorkload]):
        """
        Affiche les résultats globaux

        :param profiles_workload: Charge de travail globale par profil
        """
        text_widget = self.global_results_text
        text_widget.config(state=tk.NORMAL)

        # Titre
        text_widget.insert(tk.END, "RÉSULTATS GLOBAUX PAR PROFIL\n")
        text_widget.insert(tk.END, "==========================\n\n")

        # Récupérer tous les profils possibles
        all_profiles = {
            "Intégrateur": 0,
            "Designer": 0,
            "PMO": 0,
            "Web Backend": 0,
            "Mobile Cross": 0,
            "Mobile Android": 0,
            "Mobile iOS": 0,
            "Web front": 0,
            "DevOps": 0,
            "CTO": 0,
        }

        # Mettre à jour avec les charges de travail effectives
        for profile in profiles_workload:
            all_profiles[profile.profile] = profile.total_workload

        # Trier les profils
        sorted_profiles = sorted(all_profiles.items(), key=lambda x: x[1], reverse=True)

        # Afficher chaque profil
        for profile, workload in sorted_profiles:
            text_widget.insert(tk.END, f"Profil: {profile}\n")
            text_widget.insert(
                tk.END, f"Charge de travail totale: {workload:.2f} heures\n\n"
            )

        text_widget.config(state=tk.DISABLED)

    def _display_detailed_results(
        self, detailed_workload: Dict[str, Dict[str, List[WorkloadEntry]]]
    ):
        """
        Affiche les résultats détaillés

        :param detailed_workload: Charge de travail détaillée
        """
        text_widget = self.detailed_results_text
        text_widget.config(state=tk.NORMAL)

        # Titre
        text_widget.insert(
            tk.END, "RÉSULTATS DÉTAILLÉS PAR CHEF DE PROJET ET PAR PROJET\n"
        )
        text_widget.insert(
            tk.END, "=================================================\n\n"
        )

        # Parcourir les chefs de projet
        for pm, projects in detailed_workload.items():
            # Calculer la charge totale par profil pour ce chef de projet
            profiles_by_pm = self._calculate_profiles_workload_by_pm(pm, projects)

            # N'afficher que les chefs de projet avec des projets non vides
            if not self._has_non_empty_projects(projects):
                continue

            # Afficher le chef de projet
            text_widget.insert(tk.END, f"Chef de projet: {pm}\n")
            text_widget.insert(tk.END, "-" * 50 + "\n")

            # Profils possibles
            all_profiles = {
                "Intégrateur": 0,
                "Designer": 0,
                "PMO": 0,
                "Web Backend": 0,
                "Mobile Cross": 0,
                "Mobile Android": 0,
                "Mobile iOS": 0,
                "Web front": 0,
                "DevOps": 0,
                "CTO": 0,
            }

            # Mettre à jour avec les charges de travail effectives
            for profile_data in profiles_by_pm:
                all_profiles[profile_data["profile"]] = profile_data["total_workload"]

            # Trier les profils
            sorted_profiles = sorted(
                all_profiles.items(), key=lambda x: x[1], reverse=True
            )

            # Affichage des résultats globaux par profil pour ce chef de projet
            text_widget.insert(
                tk.END, f"RÉSULTATS GLOBAUX PAR PROFIL pour le chef de projet {pm}\n"
            )
            text_widget.insert(tk.END, "==========================\n")

            for profile, workload in sorted_profiles:
                text_widget.insert(tk.END, f"Profil: {profile}\n")
                text_widget.insert(
                    tk.END, f"Charge de travail totale: {workload:.2f} heures\n"
                )

            text_widget.insert(tk.END, "\n" + "-" * 50 + "\n\n")

            # Parcourir les projets de ce chef de projet
            for project, entries in projects.items():
                # Ne pas afficher les projets vides
                if not entries or all(entry.workload == 0 for entry in entries):
                    continue

                project_total = sum(entry.workload for entry in entries)
                text_widget.insert(
                    tk.END, f"  Projet: {project} (Total: {project_total:.2f} heures)\n"
                )

                # Trier les entrées par charge de travail décroissante
                sorted_entries = sorted(
                    [entry for entry in entries if entry.workload > 0],
                    key=lambda x: x.workload,
                    reverse=True,
                )

                # Afficher chaque entrée non nulle
                for entry in sorted_entries:
                    jira_info = (
                        f" (JIRA: {entry.jira_ticket})" if entry.jira_ticket else ""
                    )
                    text_widget.insert(
                        tk.END,
                        f"    • {entry.profile}: {entry.workload:.2f} heures{jira_info}\n",
                    )

                text_widget.insert(tk.END, "\n")

        text_widget.config(state=tk.DISABLED)

    def _calculate_profiles_workload_by_pm(
        self, pm: str, projects: Dict[str, List[WorkloadEntry]]
    ) -> List[Dict[str, Any]]:
        """
        Calcule la charge de travail par profil pour un chef de projet

        :param pm: Nom du chef de projet
        :param projects: Projets du chef de projet
        :return: Liste des charges de travail par profil
        """
        profiles_workload = {}

        for project, entries in projects.items():
            for entry in entries:
                if entry.profile not in profiles_workload:
                    profiles_workload[entry.profile] = 0
                profiles_workload[entry.profile] += entry.workload

        return [
            {"profile": profile, "total_workload": workload}
            for profile, workload in profiles_workload.items()
        ]

    def _has_non_empty_projects(self, projects: Dict[str, List[WorkloadEntry]]) -> bool:
        """
        Vérifie s'il y a des projets non vides

        :param projects: Projets à vérifier
        :return: True s'il y a des projets non vides, False sinon
        """
        return any(
            any(entry.workload > 0 for entry in project_entries)
            for project_entries in projects.values()
        )

    def has_results(self) -> bool:
        """
        Vérifie s'il y a des résultats

        :return: True s'il y a des résultats, False sinon
        """
        return bool(self._profiles_workload) and bool(self._detailed_workload)

    def get_results(
        self,
    ) -> Tuple[List[ProfileWorkload], Dict[str, Dict[str, List[WorkloadEntry]]]]:
        """
        Récupère les résultats actuels

        :return: Tuple contenant les résultats globaux et détaillés
        """
        return self._profiles_workload, self._detailed_workload
