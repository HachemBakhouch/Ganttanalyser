# Application Constants

# Excel Column Configuration
DEFAULT_START_COLUMN = "A"
DEFAULT_END_COLUMN = "Z"
DEFAULT_PROFILE_COLUMN = "E"
DEFAULT_START_ROW = 3
DEFAULT_END_ROW = 1831

# Export Options
EXPORT_FORMATS = [
    ("Fichier texte", "*.txt"),
    ("Fichier Excel", "*.xlsx"),
    ("Fichier PDF", "*.pdf"),
    ("Tous les fichiers", "*.*"),
]

# UI Configuration
APP_TITLE = "Analyseur de Charge de Travail par Profil"
DEFAULT_WINDOW_SIZE = "800x600"

# Logging Configuration
LOG_FILE = "workload_analyzer.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
