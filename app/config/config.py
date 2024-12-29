import os
from pathlib import Path

# Chemins des fichiers
DATA_DIR = Path("./data")  # Conversion en objet Path
EXCEL_PATH = DATA_DIR / "stats.xlsx"

# Ajout d'un print pour debug
print(f"Chemin du fichier Excel: {EXCEL_PATH}")

# Vérification et création du dossier data s'il n'existe pas
DATA_DIR.mkdir(exist_ok=True)


# Ajout d'un print pour debug
print(f"Chemin du fichier Excel: {EXCEL_PATH}")

# Vérification et création du dossier data s'il n'existe pas
DATA_DIR.mkdir(exist_ok=True)

# Configuration des catégories et leurs couleurs
CATEGORIES = {
    'Duel': {
        'color': "#1A78CF",
        'subcats': {
            'Duel_0': 'Duel\nPerdu',
            'Duel_1.0': 'Duel\nNeutre',
            'Duel_2.0': 'Duel\nGagné',
            'Duel_3.0': 'Duel\nDécisif',
        }
    },
    'Passe': {
        'color': "#FF9300",
        'subcats': {
            'Passe_0': 'Passe\nPerdue',
            'Passe_1.0': 'Passe\nNeutre',
            'Passe_2.0': 'Passe\nGagnée',
            'Passe_3.0': 'Passe\nDécisive',
        }
    },
    'Plaquage': {
        'color': "#D70232",
        'subcats': {
            'Plaquage_0': 'Plaquage\nPerdu',
            'Plaquage_1.0': 'Plaquage\nNeutre',
            'Plaquage_2.0': 'Plaquage\nGagné',
            'Plaquage_3.0': 'Plaquage\nDécisif',
        }
    },
    'Ruck': {
        'color': "#2ECC71",
        'subcats': {
            'Ruck_0': 'Ruck\nPerdu',
            'Ruck_1.0': 'Ruck\nNeutre',
            'Ruck_2.0': 'Ruck\nGagné',
            'Ruck_3.0': 'Ruck\nDécisif',
        }
    },
    'JAP': {
        'color': "#9B59B6",
        'subcats': {
            'JAP_0': 'JAP\nPerdu',
            'JAP_1.0': 'JAP\nNeutre',
            'JAP_2.0': 'JAP\nGagné',
            'JAP_3.0': 'JAP\nDécisif',
        }
    },
    'Reception JAP': {
        'color': "#F1C40F",
        'subcats': {
            'Réception JAP_0': 'Récep\nPerdue',
            'Réception JAP_1.0': 'Récep\nNeutre',
            'Réception JAP_2.0': 'Récep\nGagnée',
            'Réception JAP_3.0': 'Récep\nDécisive',
        }
    }
}

# Configuration du graphique
CHART_CONFIG = {
    "background_color": "#EBEBE9",
    "straight_line_color": "#EBEBE9",
    "straight_line_lw": 1,
    "last_circle_lw": 0,
    "other_circle_lw": 0,
    "inner_circle_size": 20,
    "straight_line_limit": 100,
    "figsize": (10, 10)
}

# Messages d'erreur
ERROR_MESSAGES = {
    "data_load": "Impossible de charger les données",
    "file_not_found": "Le fichier de données n'a pas été trouvé",
    "data_processing": "Erreur lors du traitement des données"
}
