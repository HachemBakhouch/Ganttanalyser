from typing import List, Dict, Any, Optional
import statistics

from src.data.data_models import WorkloadEntry, ProfileWorkload


class WorkloadCalculator:
    """
    Calculateur avancé pour l'analyse de charge de travail
    """

    @staticmethod
    def calculate_profile_workload(entries: List[WorkloadEntry]) -> ProfileWorkload:
        """
        Calcule la charge de travail pour un profil

        :param entries: Liste des entrées de charge de travail
        :return: Charge de travail du profil
        """
        if not entries:
            return ProfileWorkload(profile="Unknown", total_workload=0)

        # Profil basé sur la première entrée
        profile = entries[0].profile

        # Calcul de la charge totale
        total_workload = sum(entry.workload for entry in entries)

        return ProfileWorkload(
            profile=profile, total_workload=total_workload, projects=entries
        )

    @staticmethod
    def calculate_workload_statistics(entries: List[WorkloadEntry]) -> Dict[str, Any]:
        """
        Calcule des statistiques détaillées sur la charge de travail

        :param entries: Liste des entrées de charge de travail
        :return: Dictionnaire de statistiques
        """
        if not entries:
            return {
                "total_workload": 0,
                "average_workload": 0,
                "median_workload": 0,
                "min_workload": 0,
                "max_workload": 0,
                "workload_by_project": {},
                "workload_by_project_manager": {},
            }

        # Charge de travail totale
        total_workload = sum(entry.workload for entry in entries)

        # Calculer les charges de travail par projet
        workload_by_project = {}
        for entry in entries:
            if entry.project not in workload_by_project:
                workload_by_project[entry.project] = 0
            workload_by_project[entry.project] += entry.workload

        # Calculer les charges de travail par chef de projet
        workload_by_project_manager = {}
        for entry in entries:
            if entry.project_manager not in workload_by_project_manager:
                workload_by_project_manager[entry.project_manager] = 0
            workload_by_project_manager[entry.project_manager] += entry.workload

        # Calculs statistiques
        workloads = [entry.workload for entry in entries]

        return {
            "total_workload": total_workload,
            "average_workload": sum(workloads) / len(workloads) if workloads else 0,
            "median_workload": statistics.median(workloads) if workloads else 0,
            "min_workload": min(workloads) if workloads else 0,
            "max_workload": max(workloads) if workloads else 0,
            "workload_by_project": workload_by_project,
            "workload_by_project_manager": workload_by_project_manager,
        }

    @staticmethod
    def calculate_workload_variations(
        previous_entries: List[WorkloadEntry],
        current_entries: List[WorkloadEntry],
        threshold_percentage: float = 10.0,
    ) -> Dict[str, Any]:
        """
        Calcule les variations de charge de travail entre deux périodes

        :param previous_entries: Liste des entrées de la période précédente
        :param current_entries: Liste des entrées de la période actuelle
        :param threshold_percentage: Seuil de variation en pourcentage
        :return: Variations de charge de travail
        """
        # Grouper les entrées par profil
        prev_by_profile = WorkloadCalculator._group_entries_by_profile(previous_entries)
        curr_by_profile = WorkloadCalculator._group_entries_by_profile(current_entries)

        # Résultats des variations
        variations = {
            "significant_variations": [],
            "profiles_added": [],
            "profiles_removed": [],
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

            # Profils ajoutés
            if profile not in prev_by_profile:
                variations["profiles_added"].append(profile)
                continue

            # Profils supprimés
            if profile not in curr_by_profile:
                variations["profiles_removed"].append(profile)
                continue

            # Calculer le pourcentage de variation
            if prev_workload > 0:
                variation_pct = ((curr_workload - prev_workload) / prev_workload) * 100
            else:
                variation_pct = 100 if curr_workload > 0 else 0

            # Vérifier si la variation est significative
            if abs(variation_pct) >= threshold_percentage:
                variations["significant_variations"].append(
                    {
                        "profile": profile,
                        "previous_workload": prev_workload,
                        "current_workload": curr_workload,
                        "variation_percentage": variation_pct,
                    }
                )

        return variations

    @staticmethod
    def _group_entries_by_profile(
        entries: List[WorkloadEntry],
    ) -> Dict[str, List[WorkloadEntry]]:
        """
        Regroupe les entrées par profil

        :param entries: Liste des entrées
        :return: Dictionnaire d'entrées groupées par profil
        """
        grouped = {}
        for entry in entries:
            if entry.profile not in grouped:
                grouped[entry.profile] = []
            grouped[entry.profile].append(entry)
        return grouped

    @staticmethod
    def predict_future_workload(
        entries: List[WorkloadEntry],
        weeks_ahead: int = 4,
        smoothing_factor: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Prédit la charge de travail future basée sur les tendances historiques

        :param entries: Liste des entrées de charge de travail
        :param weeks_ahead: Nombre de semaines à prédire
        :param smoothing_factor: Facteur de lissage pour la prédiction
        :return: Prédictions de charge de travail
        """
        if not entries:
            return {
                "total_predicted_workload": 0,
                "profile_predictions": {},
                "project_predictions": {},
            }

        # Calculer les charges de travail récentes par profil
        profile_workloads = {}
        for entry in entries:
            if entry.profile not in profile_workloads:
                profile_workloads[entry.profile] = []
            profile_workloads[entry.profile].append(entry.workload)

        # Calculer les charges de travail récentes par projet
        project_workloads = {}
        for entry in entries:
            if entry.project not in project_workloads:
                project_workloads[entry.project] = []
            project_workloads[entry.project].append(entry.workload)

        # Fonction de prédiction exponentielle simple
        def predict_workload(workloads):
            if not workloads:
                return 0

            # Calcul de la moyenne mobile exponentielle
            prediction = workloads[-1]
            for w in workloads:
                prediction = smoothing_factor * w + (1 - smoothing_factor) * prediction

            # Projeter sur le nombre de semaines
            return prediction * weeks_ahead

        # Prédictions par profil
        profile_predictions = {
            profile: predict_workload(workloads)
            for profile, workloads in profile_workloads.items()
        }

        # Prédictions par projet
        project_predictions = {
            project: predict_workload(workloads)
            for project, workloads in project_workloads.items()
        }

        return {
            "total_predicted_workload": sum(profile_predictions.values()),
            "profile_predictions": profile_predictions,
            "project_predictions": project_predictions,
        }

    @staticmethod
    def analyze_workload_distribution(entries: List[WorkloadEntry]) -> Dict[str, Any]:
        """
        Analyse la distribution de la charge de travail

        :param entries: Liste des entrées de charge de travail
        :return: Analyse de distribution
        """
        if not entries:
            return {
                "total_workload": 0,
                "profile_distribution": {},
                "project_distribution": {},
                "project_manager_distribution": {},
            }

        # Distribution par profil
        profile_distribution = {}
        for entry in entries:
            if entry.profile not in profile_distribution:
                profile_distribution[entry.profile] = 0
            profile_distribution[entry.profile] += entry.workload

        # Distribution par projet
        project_distribution = {}
        for entry in entries:
            if entry.project not in project_distribution:
                project_distribution[entry.project] = 0
            project_distribution[entry.project] += entry.workload

        # Distribution par chef de projet
        project_manager_distribution = {}
        for entry in entries:
            if entry.project_manager not in project_manager_distribution:
                project_manager_distribution[entry.project_manager] = 0
            project_manager_distribution[entry.project_manager] += entry.workload

        return {
            "total_workload": sum(entry.workload for entry in entries),
            "profile_distribution": profile_distribution,
            "project_distribution": project_distribution,
            "project_manager_distribution": project_manager_distribution,
        }
