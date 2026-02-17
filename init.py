import os
import subprocess
import sys
import shutil

# ===============================
# Chemin vers l'exécutable Python 3.11
# ===============================
python_executable = sys.executable

# Vérifier si python3.11 est disponible
if shutil.which(python_executable) is None:
    print("Erreur : Python 3.11 n'est pas trouvé sur le PATH.")
    print("Veuillez installer Python 3.11 et réessayer.")
    sys.exit(1)

# ===============================
# Créer l'environnement virtuel .venv
# ===============================
venv_dir = ".venv"
if not os.path.exists(venv_dir):
    subprocess.run([python_executable, "-m", "venv", venv_dir], check=True)
    print(f"Environnement virtuel '.venv' créé avec Python 3.11")
else:
    print(f"Environnement virtuel '.venv' existe déjà")

# ===============================
# Installer les dépendances
# ===============================
pip_executable = os.path.join(venv_dir, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(venv_dir, "bin", "pip")

if os.path.exists("requirements.txt"):
    subprocess.run([pip_executable, "install", "-r", "requirements.txt"], check=True)
    print("Dépendances installées depuis requirements.txt")
else:
    print("Aucun fichier requirements.txt trouvé")
