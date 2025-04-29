from typing import List, Dict, Any, Tuple
from datetime import datetime
from src.data.data_models import WorkloadEntry, ProfileWorkload


class ComparisonService:
    """
    Service de comparaison de rapports de charge de travail
    """

    def __init__(self, settings: Dict[str, Any] = None):
        """
        Initialise le service de comparaison

        :param settings: Configuration de la comparaison
        """
        self.settings = settings or {
            "workload_threshold": 10,  # % de variation
            "new_project_threshold": 2,  # Nombre de nouveaux projets
            "priority_profiles": [],
            "weeks_to_compare": 4,
            "ignored_project_types": [],
        }

    def compare_workload_entries(
        self,
        previous_entries: List[WorkloadEntry],
        current_entries: List[WorkloadEntry],
    ) -> Dict[str, Any]:
        """
        Compare les entrées de charge de travail entre deux périodes

        :param previous_entries: Entrées de la période précédente
        :param current_entries: Entrées de la période actuelle
        :return: Résultats de la comparaison
        """
        # Dictionnaires pour faciliter la comparaison
        prev_by_profile = self._group_entries_by_profile(previous_entries)
        curr_by_profile = self._group_entries_by_profile(current_entries)

        # Résultats de la comparaison
        comparison_results = {
            "profile_changes": {},
            "new_projects": [],
            "removed_projects": [],
            "significant_workload_changes": [],
        }

        # Comparer les profils
        all_profiles = set(list(prev_by_profile.keys()) + list(curr_by_profile.keys()))

        for profile in all_profiles:
            prev_workload = sum(
                entry.workload for entry in prev_by_profile.get(profile, [])
            )
            curr_workload = sum(
                entry.workload for entry in curr_by_profile.get(profile, [])
            )

            # Calculer le changement de charge
            if prev_workload > 0:
                workload_change_pct = (
                    (curr_workload - prev_workload) / prev_workload
                ) * 100
            else:
                workload_change_pct = 100 if curr_workload > 0 else 0

            # Vérifier les changements significatifs
            if abs(workload_change_pct) >= self.settings["workload_threshold"]:
                comparison_results["profile_changes"][profile] = {
                    "previous_workload": prev_workload,
                    "current_workload": curr_workload,
                    "change_percentage": workload_change_pct,
                }

                # Ajouter aux changements significatifs si le profil est prioritaire
                if profile in self.settings.get("priority_profiles", []):
                    comparison_results["significant_workload_changes"].append(
                        {
                            "profile": profile,
                            "previous_workload": prev_workload,
                            "current_workload": curr_workload,
                            "change_percentage": workload_change_pct,
                        }
                    )

        # Identifier les nouveaux et anciens projets
        prev_projects = set(entry.project for entry in previous_entries)
        curr_projects = set(entry.project for entry in current_entries)

        comparison_results["new_projects"] = list(curr_projects - prev_projects)
        comparison_results["removed_projects"] = list(prev_projects - curr_projects)

        return comparison_results

    def _group_entries_by_profile(
        self, entries: List[WorkloadEntry]
    ) -> Dict[str, List[WorkloadEntry]]:
        """
        Regroupe les entrées par profil

        :param entries: Liste des entrées
        :return: Dictionnaire d'entrées groupées par profil
        """
        grouped = {}
        for entry in entries:
            # Ignorer les types de projets spécifiés
            if entry.project in self.settings.get("ignored_project_types", []):
                continue

            if entry.profile not in grouped:
                grouped[entry.profile] = []
            grouped[entry.profile].append(entry)

        return grouped

    def generate_comparison_report(
        self,
        previous_entries: List[WorkloadEntry],
        current_entries: List[WorkloadEntry],
    ) -> str:
        """
        Génère un rapport textuel de comparaison

        :param previous_entries: Entrées de la période précédente
        :param current_entries: Entrées de la période actuelle
        :return: Rapport de comparaison
        """
        # Effectuer la comparaison
        results = self.compare_workload_entries(previous_entries, current_entries)

        # Construire le rapport
        report = "RAPPORT DE COMPARAISON DE CHARGE DE TRAVAIL\n"
        report += "==========================================\n\n"

        # Changements de charge de travail par profil
        if results["profile_changes"]:
            report += "Changements significatifs par profil:\n"
            for profile, changes in results["profile_changes"].items():
                report += (
                    f"- {profile}: "
                    f"Charge précédente {changes['previous_workload']:.2f}h "
                    f"→ Charge actuelle {changes['current_workload']:.2f}h "
                    f"(Variation: {changes['change_percentage']:.2f}%)\n"
                )
            report += "\n"

        # Nouveaux projets
        if results["new_projects"]:
            report += "Nouveaux projets:\n"
            for project in results["new_projects"]:
                report += f"- {project}\n"
            report += "\n"

        # Projets supprimés
        if results["removed_projects"]:
            report += "Projets supprimés:\n"
            for project in results["removed_projects"]:
                report += f"- {project}\n"
            report += "\n"

        # Changements significatifs pour les profils prioritaires
        if results["significant_workload_changes"]:
            report += "Changements critiques pour les profils prioritaires:\n"
            for change in results["significant_workload_changes"]:
                report += (
                    f"- {change['profile']}: "
                    f"Charge précédente {change['previous_workload']:.2f}h "
                    f"→ Charge actuelle {change['current_workload']:.2f}h "
                    f"(Variation: {change['change_percentage']:.2f}%)\n"
                )

        return report
