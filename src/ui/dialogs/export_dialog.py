import tkinter as tk
from tkinter import filedialog, ttk
from typing import Optional

from src.data.data_models import ExportConfiguration


class ExportDialog(tk.Toplevel):
    """
    Boîte de dialogue pour l'exportation des résultats
    """

    def __init__(self, parent: tk.Tk):
        """
        Initialise la boîte de dialogue d'exportation

        :param parent: Fenêtre parente
        """
        super().__init__(parent)

        # Configuration de la fenêtre
        self.title("Exporter les résultats")
        self.geometry("400x250")
        self.resizable(False, False)

        # Variable pour stocker la configuration
        self._export_config: Optional[ExportConfiguration] = None

        # Rendre la fenêtre modale
        self.transient(parent)
        self.grab_set()

        # Créer les widgets
        self._create_widgets()

    def _create_widgets(self):
        """
        Crée les widgets de la boîte de dialogue
        """
        # Frame principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Format d'exportation
        ttk.Label(main_frame, text="Format d'exportation:").pack(
            anchor=tk.W, pady=(0, 5)
        )

        # Variable pour le format d'exportation
        self.export_format = tk.StringVar(value="txt")

        # Options de format
        formats = [
            ("Texte (.txt)", "txt"),
            ("Excel (.xlsx)", "xlsx"),
            ("PDF (.pdf)", "pdf"),
        ]

        for text, value in formats:
            ttk.Radiobutton(
                main_frame, text=text, variable=self.export_format, value=value
            ).pack(anchor=tk.W, padx=20)

        # Sélection de fichier
        ttk.Label(main_frame, text="Fichier de destination:").pack(
            anchor=tk.W, pady=(10, 5)
        )

        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(
            file_frame, textvariable=self.file_path_var, width=40
        )
        self.file_path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        browse_button = ttk.Button(
            file_frame, text="Parcourir", command=self._browse_file
        )
        browse_button.pack(side=tk.RIGHT)

        # Boutons OK et Annuler
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(
            side=tk.RIGHT, padx=5
        )
        ttk.Button(button_frame, text="Annuler", command=self.destroy).pack(
            side=tk.RIGHT
        )

    def _browse_file(self):
        """
        Ouvre une boîte de dialogue pour sélectionner un fichier de destination
        """
        # Définir l'extension et les types de fichiers en fonction du format
        format_type = self.export_format.get()

        # Dictionnaire des types de fichiers
        file_types = {
            "txt": [("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
            "xlsx": [("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")],
            "pdf": [("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")],
        }

        # Boîte de dialogue de sauvegarde
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=file_types.get(format_type, [("Tous les fichiers", "*.*")]),
        )

        if file_path:
            self.file_path_var.set(file_path)

    def _on_ok(self):
        """
        Traite la validation de la boîte de dialogue
        """
        file_path = self.file_path_var.get().strip()

        if not file_path:
            tk.messagebox.showwarning(
                "Attention", "Veuillez sélectionner un fichier de destination."
            )
            return

        # Créer la configuration d'exportation
        self._export_config = ExportConfiguration(
            export_format=self.export_format.get(), file_path=file_path
        )

        # Fermer la boîte de dialogue
        self.destroy()

    def show(self) -> Optional[ExportConfiguration]:
        """
        Affiche la boîte de dialogue et attend la sélection

        :return: Configuration d'exportation ou None si annulé
        """
        # Attendre que la boîte de dialogue soit fermée
        self.wait_window(self)

        return self._export_config
