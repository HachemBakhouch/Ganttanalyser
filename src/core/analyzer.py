from typing import List, Dict, Any
from src.data.repository import WorkloadRepository
from src.data.data_models import AnalysisConfiguration, ProfileWorkload, WorkloadEntry


class WorkloadAnalyzer:
    def __init__(self, repository: WorkloadRepository):
        """
        Initialise l'analyseur de charge de travail

        :param repository: Dépôt de données de charge de travail
        """
        self.repository = repository

    def analyze_global_workload(
        self, config: AnalysisConfiguration
    ) -> List[ProfileWorkload]:
        """
        Analyse la charge de travail globale par profil

        :param config: Configuration pour l'analyse
        :return: Liste des charges de travail par profil
        """
        return self.repository.get_profiles_workload(config)

    def analyze_detailed_workload(
        self, config: AnalysisConfiguration
    ) -> Dict[str, Dict[str, List[WorkloadEntry]]]:
        """
        Analyse la charge de travail détaillée par chef de projet et projet

        :param config: Configuration pour l'analyse
        :return: Dictionnaire hiérarchique de la charge de travail
        """
        return self.repository.get_detailed_workload_by_project_manager(config)

    def filter_workload_by_profiles(
        self, config: AnalysisConfiguration, selected_profiles: List[str]
    ) -> List[ProfileWorkload]:
        """
        Filtre la charge de travail pour des profils spécifiques

        :param config: Configuration pour l'analyse
        :param selected_profiles: Liste des profils à filtrer
        :return: Liste des charges de travail pour les profils sélectionnés
        """
        config.selected_profiles = selected_profiles
        return self.repository.get_profiles_workload(config)

    def calculate_total_workload(self, config: AnalysisConfiguration) -> float:
        """
        Calcule la charge de travail totale

        :param config: Configuration pour l'analyse
        :return: Charge de travail totale
        """
        profiles_workload = self.analyze_global_workload(config)
        return sum(profile.total_workload for profile in profiles_workload)
