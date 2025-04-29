import sys
import tkinter as tk
from typing import Optional


def main() -> Optional[int]:
    """
    Point d'entrée principal de l'application

    :return: Code de sortie (0 pour succès, autre chose en cas d'erreur)
    """
    try:
        # Importer ici pour éviter les imports potentiellement problématiques
        from src.ui.main_window import ExcelProfileAnalyzerApp

        # Créer la fenêtre racine Tkinter
        root = tk.Tk()

        # Personnaliser l'apparence de la fenêtre
        root.title("Analyseur de Charge de Travail")

        # Initialiser l'application
        app = ExcelProfileAnalyzerApp(root)

        # Lancer la boucle d'événements Tkinter
        root.mainloop()

        return 0

    except ImportError as e:
        print(f"Erreur d'importation : {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Erreur lors du lancement de l'application : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
