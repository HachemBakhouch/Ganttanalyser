from typing import List, Dict, Any
from src.data.excel_reader import ExcelReader
from src.data.data_models import WorkloadEntry, AnalysisConfiguration, ProfileWorkload


class WorkloadRepository:
    def __init__(self, excel_reader: ExcelReader):
        """
        Initialise le dépôt de données de charge de travail

        :param excel_reader: Instance du lecteur Excel
        """
        self.excel_reader = excel_reader

    def get_all_workload_entries(
        self, config: AnalysisConfiguration, min_workload: float = 0.01
    ) -> List[WorkloadEntry]:
        """
        Récupère toutes les entrées de charge de travail significatives

        :param config: Configuration pour la lecture
        :param min_workload: Charge de travail minimale à considérer
        :return: Liste des entrées de charge de travail
        """
        all_entries = self.excel_reader.read_workload_entries(config)
        return [entry for entry in all_entries if entry.workload >= min_workload]

    def get_profiles_workload(
        self, config: AnalysisConfiguration, min_workload: float = 0.01
    ) -> List[ProfileWorkload]:
        """
        Calcule la charge de travail par profil en filtrant les projets significatifs

        :param config: Configuration pour la lecture
        :param min_workload: Charge de travail minimale à considérer
        :return: Liste des charges de travail par profil
        """
        workload_entries = self.get_all_workload_entries(config, min_workload)

        # Regroupement par profil
        profiles_workload = {}

        for entry in workload_entries:
            if entry.profile not in profiles_workload:
                profiles_workload[entry.profile] = ProfileWorkload(
                    profile=entry.profile, total_workload=0, projects=[]
                )

            profile_data = profiles_workload[entry.profile]
            profile_data.total_workload += entry.workload
            profile_data.projects.append(entry)

        return list(profiles_workload.values())

    def get_detailed_workload_by_project_manager(
        self, config: AnalysisConfiguration, min_workload: float = 0.01
    ) -> Dict[str, Dict[str, List[WorkloadEntry]]]:
        """
        Récupère la charge de travail détaillée par chef de projet et par projet
        Filtre les projets avec une charge de travail significative

        :param config: Configuration pour la lecture
        :param min_workload: Charge de travail minimale à considérer
        :return: Dictionnaire hiérarchique de la charge de travail
        """
        workload_entries = self.get_all_workload_entries(config, min_workload)

        # Regroupement par chef de projet, puis par projet
        detailed_workload = {}

        for entry in workload_entries:
            if entry.project_manager not in detailed_workload:
                detailed_workload[entry.project_manager] = {}

            if entry.project not in detailed_workload[entry.project_manager]:
                detailed_workload[entry.project_manager][entry.project] = []

            detailed_workload[entry.project_manager][entry.project].append(entry)

        # Filtrer pour ne garder que les chefs de projet et projets avec une charge significative
        return detailed_workload


from typing import List, Dict, Any
from src.data.excel_reader import ExcelReader
from src.data.data_models import WorkloadEntry, AnalysisConfiguration, ProfileWorkload


class WorkloadRepository:
    def __init__(self, excel_reader: ExcelReader):
        """
        Initialise le dépôt de données de charge de travail

        :param excel_reader: Instance du lecteur Excel
        """
        self.excel_reader = excel_reader

    def get_all_workload_entries(
        self, config: AnalysisConfiguration, min_workload: float = 0.01
    ) -> List[WorkloadEntry]:
        """
        Récupère toutes les entrées de charge de travail avec un seuil minimal

        :param config: Configuration pour la lecture
        :param min_workload: Charge de travail minimale à considérer
        :return: Liste des entrées de charge de travail
        """
        all_entries = self.excel_reader.read_workload_entries(config)
        return [entry for entry in all_entries if entry.workload >= min_workload]

    def get_profiles_workload(
        self, config: AnalysisConfiguration, min_workload: float = 0.01
    ) -> List[ProfileWorkload]:
        """
        Calcule la charge de travail par profil en filtrant les projets significatifs

        :param config: Configuration pour la lecture
        :param min_workload: Charge de travail minimale à considérer
        :return: Liste des charges de travail par profil
        """
        workload_entries = self.get_all_workload_entries(config, min_workload)

        # Regroupement par profil
        profiles_workload = {}

        for entry in workload_entries:
            if entry.profile not in profiles_workload:
                profiles_workload[entry.profile] = ProfileWorkload(
                    profile=entry.profile, total_workload=0, projects=[]
                )

            profile_data = profiles_workload[entry.profile]
            profile_data.total_workload += entry.workload
            profile_data.projects.append(entry)

        return list(profiles_workload.values())

    def get_detailed_workload_by_project_manager(
        self, config: AnalysisConfiguration, min_workload: float = 0.01
    ) -> Dict[str, Dict[str, List[WorkloadEntry]]]:
        """
        Récupère la charge de travail détaillée par chef de projet et par projet
        Filtre les projets avec une charge de travail significative

        :param config: Configuration pour la lecture
        :param min_workload: Charge de travail minimale à considérer
        :return: Dictionnaire hiérarchique de la charge de travail
        """
        workload_entries = self.get_all_workload_entries(config, min_workload)

        # Regroupement par chef de projet, puis par projet
        detailed_workload = {}

        for entry in workload_entries:
            if entry.project_manager not in detailed_workload:
                detailed_workload[entry.project_manager] = {}

            if entry.project not in detailed_workload[entry.project_manager]:
                detailed_workload[entry.project_manager][entry.project] = []

            detailed_workload[entry.project_manager][entry.project].append(entry)

        # Filtrer pour ne garder que les chefs de projet et projets avec une charge significative
        return {
            pm: {
                project: entries
                for project, entries in projects.items()
                if sum(entry.workload for entry in entries) >= min_workload
            }
            for pm, projects in detailed_workload.items()
            if any(
                sum(entry.workload for entry in entries) >= min_workload
                for entries in projects.values()
            )
        }


from typing import List, Dict, Any
from src.data.excel_reader import ExcelReader
from src.data.data_models import WorkloadEntry, AnalysisConfiguration, ProfileWorkload


class WorkloadRepository:
    def __init__(self, excel_reader: ExcelReader):
        """
        Initialise le dépôt de données de charge de travail

        :param excel_reader: Instance du lecteur Excel
        """
        self.excel_reader = excel_reader

    def get_all_workload_entries(
        self, config: AnalysisConfiguration
    ) -> List[WorkloadEntry]:
        """
        Récupère toutes les entrées de charge de travail

        :param config: Configuration pour la lecture
        :return: Liste des entrées de charge de travail
        """
        return self.excel_reader.read_workload_entries(config)

    def get_profiles_workload(
        self, config: AnalysisConfiguration
    ) -> List[ProfileWorkload]:
        """
        Calcule la charge de travail par profil

        :param config: Configuration pour la lecture
        :return: Liste des charges de travail par profil
        """
        workload_entries = self.get_all_workload_entries(config)

        # Regroupement par profil
        profiles_workload = {}

        for entry in workload_entries:
            if entry.profile not in profiles_workload:
                profiles_workload[entry.profile] = ProfileWorkload(
                    profile=entry.profile, total_workload=0, projects=[]
                )

            profile_data = profiles_workload[entry.profile]
            profile_data.total_workload += entry.workload
            profile_data.projects.append(entry)

        return list(profiles_workload.values())

    def get_detailed_workload_by_project_manager(
        self, config: AnalysisConfiguration
    ) -> Dict[str, Dict[str, List[WorkloadEntry]]]:
        """
        Récupère la charge de travail détaillée par chef de projet et par projet

        :param config: Configuration pour la lecture
        :return: Dictionnaire hiérarchique de la charge de travail
        """
        workload_entries = self.get_all_workload_entries(config)

        # Regroupement par chef de projet, puis par projet
        detailed_workload = {}

        for entry in workload_entries:
            if entry.project_manager not in detailed_workload:
                detailed_workload[entry.project_manager] = {}

            if entry.project not in detailed_workload[entry.project_manager]:
                detailed_workload[entry.project_manager][entry.project] = []

            detailed_workload[entry.project_manager][entry.project].append(entry)

        return detailed_workload
