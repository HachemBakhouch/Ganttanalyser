import re
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.data.data_models import WorkloadEntry, AnalysisConfiguration
from src.data.excel_reader import ExcelReader


class WorkloadExtractor:
    """
    Extracteur de données de charge de travail avec des capacités avancées
    """

    def __init__(self, excel_reader: ExcelReader):
        """
        Initialise l'extracteur avec un lecteur Excel

        :param excel_reader: Instance du lecteur Excel
        """
        self.excel_reader = excel_reader

    def extract_workload_entries(
        self,
        config: AnalysisConfiguration,
        additional_filters: Optional[Dict[str, Any]] = None,
    ) -> List[WorkloadEntry]:
        """
        Extrait les entrées de charge de travail avec des filtres personnalisables

        :param config: Configuration de l'analyse
        :param additional_filters: Filtres supplémentaires pour l'extraction
        :return: Liste des entrées de charge de travail
        """
        # Lire toutes les entrées de la feuille
        all_entries = self._read_raw_entries(config)

        # Appliquer les filtres supplémentaires
        if additional_filters:
            all_entries = self._apply_filters(all_entries, additional_filters)

        return all_entries

    def _read_raw_entries(self, config: AnalysisConfiguration) -> List[WorkloadEntry]:
        """
        Lit les entrées brutes du fichier Excel

        :param config: Configuration de l'analyse
        :return: Liste des entrées brutes
        """
        workload_entries = []

        # Parcourir les lignes spécifiées
        for row in range(config.start_row, config.end_row + 1):
            try:
                # Extraire les valeurs des colonnes nécessaires
                project_manager = self._get_cell_value(
                    row, "B"
                )  # Colonne chef de projet
                project = self._get_cell_value(row, "D")  # Colonne projet
                profile = self._get_cell_value(row, config.profile_column)
                jira_ticket = self._get_cell_value(row, "F")  # Colonne ticket JIRA

                # Calculer la charge de travail
                workload = self._calculate_workload(row, config)

                # Créer une entrée si toutes les informations essentielles sont présentes
                if project_manager and project and profile:
                    entry = WorkloadEntry(
                        project_manager=str(project_manager),
                        project=str(project),
                        profile=str(profile),
                        jira_ticket=str(jira_ticket) if jira_ticket else None,
                        workload=workload,
                    )
                    workload_entries.append(entry)

            except Exception as e:
                # Gérer les erreurs d'extraction sans interrompre le processus
                print(f"Erreur lors de l'extraction de la ligne {row}: {str(e)}")

        return workload_entries

    def _get_cell_value(self, row: int, column: str) -> Optional[str]:
        """
        Récupère la valeur d'une cellule spécifique

        :param row: Numéro de ligne
        :param column: Lettre de colonne
        :return: Valeur de la cellule
        """
        try:
            column_index = self.excel_reader._column_index_from_string(column)
            cell = self.excel_reader.sheet.cell(row=row, column=column_index)
            return cell.value
        except Exception:
            return None

    def _calculate_workload(self, row: int, config: AnalysisConfiguration) -> float:
        """
        Calcule la charge de travail pour une ligne

        :param row: Numéro de ligne
        :param config: Configuration de l'analyse
        :return: Charge de travail totale
        """
        start_col_index = self.excel_reader._column_index_from_string(
            config.start_column
        )
        end_col_index = self.excel_reader._column_index_from_string(config.end_column)

        total_workload = 0
        for col in range(start_col_index, end_col_index + 1):
            cell = self.excel_reader.sheet.cell(row=row, column=col)
            if cell.value is not None and isinstance(cell.value, (int, float)):
                total_workload += cell.value

        return total_workload

    def _apply_filters(
        self, entries: List[WorkloadEntry], filters: Dict[str, Any]
    ) -> List[WorkloadEntry]:
        """
        Applique des filtres personnalisés aux entrées

        :param entries: Liste des entrées
        :param filters: Dictionnaire de filtres
        :return: Liste des entrées filtrées
        """
        filtered_entries = entries.copy()

        # Filtre par profil
        if "profiles" in filters:
            filtered_entries = [
                entry
                for entry in filtered_entries
                if entry.profile in filters["profiles"]
            ]

        # Filtre par projet
        if "projects" in filters:
            filtered_entries = [
                entry
                for entry in filtered_entries
                if entry.project in filters["projects"]
            ]

        # Filtre par chef de projet
        if "project_managers" in filters:
            filtered_entries = [
                entry
                for entry in filtered_entries
                if entry.project_manager in filters["project_managers"]
            ]

        # Filtre par charge de travail minimale
        if "min_workload" in filters:
            filtered_entries = [
                entry
                for entry in filtered_entries
                if entry.workload >= filters["min_workload"]
            ]

        # Filtre par charge de travail maximale
        if "max_workload" in filters:
            filtered_entries = [
                entry
                for entry in filtered_entries
                if entry.workload <= filters["max_workload"]
            ]

        return filtered_entries

    def extract_unique_metadata(self) -> Dict[str, List[str]]:
        """
        Extrait les métadonnées uniques du fichier

        :return: Dictionnaire des métadonnées uniques
        """
        unique_metadata = {
            "profiles": set(),
            "projects": set(),
            "project_managers": set(),
            "jira_tickets": set(),
        }

        # Parcourir toutes les entrées
        for row in range(3, self.excel_reader.sheet.max_row + 1):
            unique_metadata["profiles"].add(str(self._get_cell_value(row, "E") or ""))
            unique_metadata["projects"].add(str(self._get_cell_value(row, "D") or ""))
            unique_metadata["project_managers"].add(
                str(self._get_cell_value(row, "B") or "")
            )
            unique_metadata["jira_tickets"].add(
                str(self._get_cell_value(row, "F") or "")
            )

        # Convertir les ensembles en listes et supprimer les valeurs vides
        for key in unique_metadata:
            unique_metadata[key] = sorted(list(filter(bool, unique_metadata[key])))

        return unique_metadata
