import tkinter as tk
from tkinter import filedialog, ttk
from typing import Callable, Optional


class FileSelector(ttk.Frame):
    """
    Composant pour la sélection de fichiers Excel
    """

    def __init__(self, master: tk.Tk, on_file_selected: Callable[[str], None]):
        """
        Initialise le sélecteur de fichiers

        :param master: Widget parent
        :param on_file_selected: Fonction de callback lors de la sélection d'un fichier
        """
        super().__init__(master, style="TFrame")

        self.on_file_selected = on_file_selected
        self.file_path: Optional[str] = None

        # Créer les widgets
        self._create_widgets()

    def _create_widgets(self):
        """
        Crée les widgets du sélecteur de fichiers
        """
        # Titre de la section
        self.file_label = ttk.Label(self, text="Fichier Excel", style="TLabel")
        self.file_label.pack(side=tk.LEFT, padx=5)

        # Chemin du fichier
        self.file_path_label = ttk.Label(
            self, text="Aucun fichier sélectionné", width=50, style="TLabel"
        )
        self.file_path_label.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Bouton de sélection
        self.select_button = ttk.Button(
            self, text="Sélectionner", command=self._select_file
        )
        self.select_button.pack(side=tk.RIGHT, padx=5)

    def _select_file(self):
        """
        Ouvre une boîte de dialogue pour sélectionner un fichier Excel
        """
        file_path = filedialog.askopenfilename(
            title="Sélectionner un fichier Excel",
            filetypes=[
                ("Fichiers Excel", "*.xlsx *.xls"),
                ("Tous les fichiers", "*.*"),
            ],
        )

        if file_path:
            # Mettre à jour l'affichage
            self.file_path = file_path
            self.file_path_label.config(text=file_path)

            # Appeler le callback
            if self.on_file_selected:
                self.on_file_selected(file_path)
