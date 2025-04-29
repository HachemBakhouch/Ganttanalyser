import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional

from src.constants import (
    APP_TITLE,
    DEFAULT_WINDOW_SIZE,
    DEFAULT_START_COLUMN,
    DEFAULT_END_COLUMN,
    DEFAULT_PROFILE_COLUMN,
    DEFAULT_START_ROW,
    DEFAULT_END_ROW,
    EXPORT_FORMATS,
)
from src.data.data_models import AnalysisConfiguration, ExportConfiguration
from src.data.excel_reader import ExcelReader
from src.data.repository import WorkloadRepository
from src.core.analyzer import WorkloadAnalyzer
from src.services.export_service import ExportService
from src.ui.components.file_selector import FileSelector
from src.ui.components.profile_manager import ProfileManager
from src.ui.components.results_display import ResultsDisplay
from src.ui.dialogs.export_dialog import ExportDialog


class ExcelProfileAnalyzerApp:
    def __init__(self, root: tk.Tk):
        """
        Initialise l'application principale

        :param root: Fenêtre racine Tkinter
        """
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.resizable(True, True)

        # Variables d'état
        self.file_path: Optional[str] = None
        self.excel_reader: Optional[ExcelReader] = None
        self.workload_repository: Optional[WorkloadRepository] = None
        self.workload_analyzer: Optional[WorkloadAnalyzer] = None
        self.export_service: ExportService = ExportService()

        # Configuration par défaut
        self.config = AnalysisConfiguration(
            start_column=DEFAULT_START_COLUMN,
            end_column=DEFAULT_END_COLUMN,
            profile_column=DEFAULT_PROFILE_COLUMN,
            start_row=DEFAULT_START_ROW,
            end_row=DEFAULT_END_ROW,
        )

        # Création des composants
        self._create_main_layout()

    def _create_main_layout(self):
        """
        Crée la disposition principale de l'interface
        """
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sélecteur de fichier
        self.file_selector = FileSelector(main_frame, self._on_file_selected)
        self.file_selector.pack(fill=tk.X, pady=5)

        # Configuration de la plage
        range_frame = self._create_range_configuration_frame(main_frame)
        range_frame.pack(fill=tk.X, pady=5)

        # Gestionnaire de profils
        self.profile_manager = ProfileManager(main_frame, self._on_profiles_updated)
        self.profile_manager.pack(fill=tk.BOTH, expand=True, pady=5)

        # Affichage des résultats
        self.results_display = ResultsDisplay(main_frame)
        self.results_display.pack(fill=tk.BOTH, expand=True, pady=5)

        # Frame des boutons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        # Bouton de calcul
        calculate_button = ttk.Button(
            buttons_frame,
            text="Calculer la charge de travail",
            command=self._calculate_workload,
        )
        calculate_button.pack(side=tk.LEFT, padx=5)

        # Bouton d'exportation
        export_button = ttk.Button(
            buttons_frame,
            text="Exporter les résultats",
            command=self._export_results,
            state=tk.DISABLED,
        )
        export_button.pack(side=tk.LEFT, padx=5)
        self.export_button = export_button

    def _create_range_configuration_frame(self, parent):
        """
        Crée le frame de configuration des plages de colonnes et lignes

        :param parent: Widget parent
        :return: Frame de configuration
        """
        range_frame = ttk.LabelFrame(parent, text="Plage de colonnes à analyser")

        # Colonne de début
        ttk.Label(range_frame, text="De la colonne:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.start_col_entry = ttk.Entry(range_frame, width=5)
        self.start_col_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.start_col_entry.insert(0, DEFAULT_START_COLUMN)

        # Colonne de fin
        ttk.Label(range_frame, text="À la colonne:").grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.W
        )
        self.end_col_entry = ttk.Entry(range_frame, width=5)
        self.end_col_entry.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.end_col_entry.insert(0, DEFAULT_END_COLUMN)

        # Colonne de profil
        ttk.Label(range_frame, text="Colonne des profils:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.profile_col_entry = ttk.Entry(range_frame, width=5)
        self.profile_col_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.profile_col_entry.insert(0, DEFAULT_PROFILE_COLUMN)

        # Ligne de début
        ttk.Label(range_frame, text="Première ligne:").grid(
            row=1, column=2, padx=5, pady=5, sticky=tk.W
        )
        self.start_row_entry = ttk.Entry(range_frame, width=5)
        self.start_row_entry.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        self.start_row_entry.insert(0, str(DEFAULT_START_ROW))

        # Ligne de fin
        ttk.Label(range_frame, text="Dernière ligne:").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W
        )
        self.end_row_entry = ttk.Entry(range_frame, width=5)
        self.end_row_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.end_row_entry.insert(0, str(DEFAULT_END_ROW))

        return range_frame

    def _on_file_selected(self, file_path: str):
        """
        Gère la sélection d'un fichier Excel

        :param file_path: Chemin du fichier sélectionné
        """
        try:
            # Charger le fichier Excel
            self.file_path = file_path
            self.excel_reader = ExcelReader(file_path)

            # Extraire les profils automatiquement
            self.config.profile_column = self.profile_col_entry.get().strip().upper()
            self.config.start_row = int(self.start_row_entry.get())
            self.config.end_row = int(self.end_row_entry.get())

            # Extraire les profils uniques
            unique_profiles = self.excel_reader.extract_unique_profiles(self.config)

            # Mettre à jour le gestionnaire de profils
            self.profile_manager.set_available_profiles(unique_profiles)

            # Initialiser le dépôt et l'analyseur
            self.workload_repository = WorkloadRepository(self.excel_reader)
            self.workload_analyzer = WorkloadAnalyzer(self.workload_repository)

            messagebox.showinfo("Succès", f"Fichier {file_path} chargé avec succès!")

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible de charger le fichier: {str(e)}"
            )
            self.file_path = None
            self.excel_reader = None

    def _on_profiles_updated(self, selected_profiles: List[str]):
        """
        Met à jour la configuration avec les profils sélectionnés

        :param selected_profiles: Liste des profils sélectionnés
        """
        self.config.selected_profiles = selected_profiles

    def _calculate_workload(self):
        """
        Calcule la charge de travail selon la configuration actuelle
        """
        if not self.excel_reader or not self.workload_analyzer:
            messagebox.showwarning(
                "Attention", "Veuillez d'abord charger un fichier Excel."
            )
            return

        try:
            # Mettre à jour la configuration à partir des entrées
            self.config.start_column = self.start_col_entry.get().strip().upper()
            self.config.end_column = self.end_col_entry.get().strip().upper()
            self.config.profile_column = self.profile_col_entry.get().strip().upper()
            self.config.start_row = int(self.start_row_entry.get())
            self.config.end_row = int(self.end_row_entry.get())

            # Analyser la charge de travail
            profiles_workload = self.workload_analyzer.analyze_global_workload(
                self.config
            )
            detailed_workload = self.workload_analyzer.analyze_detailed_workload(
                self.config
            )

            # Afficher les résultats
            self.results_display.display_results(profiles_workload, detailed_workload)

            # Activer le bouton d'exportation
            self.export_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Erreur lors du calcul de la charge de travail: {str(e)}"
            )

    def _export_results(self):
        """
        Ouvre la boîte de dialogue d'exportation
        """
        if not self.results_display.has_results():
            messagebox.showwarning("Attention", "Aucun résultat à exporter.")
            return

        # Ouvrir la boîte de dialogue d'exportation
        export_dialog = ExportDialog(self.root)
        export_config = export_dialog.show()

        if export_config:
            try:
                # Récupérer les résultats actuels
                profiles_workload, detailed_workload = (
                    self.results_display.get_results()
                )

                # Exporter les résultats
                self.export_service.export(
                    export_config, profiles_workload, detailed_workload
                )

                messagebox.showinfo(
                    "Succès",
                    f"Résultats exportés avec succès en {export_config.export_format}!",
                )

            except Exception as e:
                messagebox.showerror(
                    "Erreur", f"Erreur lors de l'exportation: {str(e)}"
                )
