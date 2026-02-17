import os
import sys
import subprocess
from pathlib import Path

# ===============================
# Vérification version Python
# ===============================
if sys.version_info < (3, 11):
    print("Erreur : Python 3.11 minimum requis.")
    sys.exit(1)

# ===============================
# Création de l'environnement virtuel
# ===============================
venv_path = Path(".venv")

if not venv_path.exists():
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    print("✅ Environnement virtuel créé")
else:
    print("ℹ️ Environnement virtuel déjà existant")

# ===============================
# Détection pip
# ===============================
if os.name == "nt":
    pip_path = venv_path / "Scripts" / "pip.exe"
else:
    pip_path = venv_path / "bin" / "pip"

# ===============================
# Mise à jour pip + installation
# ===============================
subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)

requirements = Path("requirements.txt")

if requirements.exists():
    subprocess.run([str(pip_path), "install", "-r", str(requirements)], check=True)
    print("✅ Dépendances installées")
else:
    print("⚠️ Aucun requirements.txt trouvé")

