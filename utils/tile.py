# Boucle sur une liste d'images et crée une version avec des tuiles
import os
import subprocess

def extraire_fichiers_tif(chemin_fichier):
    """
    Extrait les fichiers se terminant par .tif à partir d'un fichier texte.

    :param chemin_fichier: Chemin du fichier à lire
    :return: Liste des chemins complets des fichiers .tif
    """
    fichiers_tif = []
    dossier_courant = ""

    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                
                # Identifier le dossier courant
                if ligne.startswith("Dossier :"):
                    dossier_courant = ligne.replace("Dossier :", "").strip()

                # Identifier les fichiers [Fichier] se terminant par .tif
                elif ligne.startswith("[Fichier]") and (ligne.lower().endswith(".tif") or ligne.lower().endswith(".tiff")):
                    fichier_tif = ligne.replace("[Fichier]", "").strip()
                    chemin_complet = f"{dossier_courant}/{fichier_tif}"
                    fichiers_tif.append(chemin_complet)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {chemin_fichier} est introuvable.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

    return fichiers_tif


if __name__ == "__main__":
    # Remplacez 'chemin_du_fichier.txt' par le chemin réel de votre fichier
    chemin_fichier = "fichiers.txt"
    fichiers = extraire_fichiers_tif(chemin_fichier)

    if fichiers:
        for fichier in fichiers:

            # Étape 1 : Extraire le numéro de dossier (avant le tiret) depuis le chemin original
            numero_dossier = fichier.split("/")[3].split(" - ")[0]

            # Étape 2 : Extraire le nom du fichier (après le dernier '/')
            nom_fichier = fichier.split("/")[-1]
            if nom_fichier.endswith(".tiff"):
                nom_fichier = nom_fichier.replace(".tiff", ".tif")

            # Étape 3 : Construire le nouveau chemin
            nouveau_chemin = f"/Volumes/tresors/iiif/{numero_dossier}/{nom_fichier}"

            # Étape 4: Créer le dossier
            os.makedirs(f"/Volumes/tresors/iiif/{numero_dossier}", exist_ok=True)

            # Étape 5: Créer le .tiff
            commande = ["vips", "tiffsave", fichier, nouveau_chemin, "--tile", "--pyramid", "--compression", "lzw", "--tile-width", "512", "--tile-height", "512"]
            try:
                subprocess.run(commande, check=True)
                print(f"{fichier} = {nouveau_chemin}")
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'exécution de la commande : {e}")
            except FileNotFoundError:
                print("Erreur : La commande 'vips' n'a pas été trouvée. Assurez-vous que vips est installé et accessible depuis le PATH.")
