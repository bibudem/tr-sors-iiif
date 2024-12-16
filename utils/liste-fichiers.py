# Lit un partage et génère un fichier qui liste tous les
# fichiers trouvés
import os
import subprocess
import sys

def monter_partage_smb(smb_url, point_de_montage):
    """
    Monte un partage SMB sur macOS.
    """
    if not os.path.exists(point_de_montage):
        os.makedirs(point_de_montage)  # Crée le point de montage si nécessaire

    try:
        # Monte le partage SMB
        subprocess.run(
            ["mount", "-t", "smbfs", smb_url, point_de_montage],
            check=True
        )
        print(f"Partage SMB monté sur {point_de_montage}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du montage du partage SMB : {e}")
        sys.exit(1)

def demonter_partage(point_de_montage):
    """
    Démonte le partage monté.
    """
    try:
        subprocess.run(["umount", point_de_montage], check=True)
        print(f"Partage démonté de {point_de_montage}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du démontage du partage : {e}")

def lister_fichiers(point_de_montage):
    """
    Liste les fichiers et dossiers dans le point de montage.
    """
    for root, dirs, files in os.walk(point_de_montage):
        print(f"Dossier : {root}")
        for dossier in dirs:
            print(f"  [Dossier] {dossier}")
        for fichier in files:
            print(f"  [Fichier] {fichier}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python script.py smb://utilisateur@ordinateur.nom/racine point_de_montage_local")
        sys.exit(1)

    smb_url = sys.argv[1]       # Exemple : smb://user@host/share
    point_de_montage = sys.argv[2]  # Exemple : /Volumes/mon_partage

    try:
        # Monter le partage SMB
        monter_partage_smb(smb_url, point_de_montage)

        # Lister les fichiers et dossiers
        print("\nListe des fichiers et dossiers :")
        lister_fichiers(point_de_montage)
    finally:
        # Démonter le partage à la fin
        demonter_partage(point_de_montage)
