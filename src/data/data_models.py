from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class WorkloadEntry:
    """
    Représente une entrée de charge de travail dans le fichier Excel
    """

    project_manager: str
    project: str
    profile: str
    jira_ticket: Optional[str] = None
    workload: float = 0.0


@dataclass
class ProfileWorkload:
    """
    Représente la charge de travail totale pour un profil
    """

    profile: str
    total_workload: float = 0.0
    projects: List[WorkloadEntry] = field(default_factory=list)


@dataclass
class AnalysisConfiguration:
    """
    Configuration pour l'analyse de charge de travail
    """

    start_column: str = "A"
    end_column: str = "Z"
    profile_column: str = "E"
    start_row: int = 3
    end_row: int = 1831
    selected_profiles: List[str] = field(default_factory=list)


@dataclass
class ExportConfiguration:
    """
    Configuration pour l'exportation des résultats
    """

    export_format: str = "txt"
    file_path: Optional[str] = None
