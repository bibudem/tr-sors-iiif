# Création d'un squelette de manifest depuis une liste de fichier
# et le serveur d'images IIIF
import os
import sys
from iiif_prezi3 import Manifest, config

# Quelques variables utiles
iiif_server_base_url = "https://pvj5vvaturp6mtjbgb55ug76eq0fokec.lambda-url.ca-central-1.on.aws/iiif/3/"
manifest_base_id = "https://bibudem.github.io/tresors-iiif/manifests/"
fichier_dossiers = "dossiers.txt"
fichier_fichiers = "fichiers_tile.txt"
dossier_manifest = "manifests-auto"

# On va lire les dossiers à traiter
try:
    with open(fichier_dossiers, "r", encoding="utf-8") as dossiers:
        for dossier in dossiers:
            dossier = dossier.strip()

            # On va créer un nouveau manifest
            manifest_root_id = f"{manifest_base_id}{dossier}"
            manifest_id = f"{manifest_root_id}.json"
            print(f"ID du Manifest = {manifest_id}")
            manifest = Manifest(id=manifest_id, label={"fr": [dossier]})

            # On va lire le fichier des fichiers et traiter uniquement ceux qui nous concernent
            with open(fichier_fichiers, "r", encoding="utf8") as fichiers:
                for fichier in fichiers:
                    fichier = fichier.strip()
                    if dossier in fichier:
                        if (fichier.find("=") != -1):
                            fichier = fichier.split("=")[1].strip()
                            fichier = fichier.split("/")[5]
                            fichier_sans_extension = fichier.split(".")[0]
                            page = fichier_sans_extension.split("_p")[1]
                            manifest.make_canvas_from_iiif(
                                url = f"{iiif_server_base_url}{fichier_sans_extension}",
                                id = f"{manifest_root_id}/canvas/p{page}",
                                label = f"Page {page}",
                                anno_id = f"{manifest_root_id}/annotation/p{page}-image",
                                anno_page_id = f"{manifest_root_id}/page/p{page}/1"
                            )
#                        print(f"""
#                              url =          {iiif_server_base_url}{fichier_sans_extension}
#                              id =           {manifest_root_id}/canvas/p{page}
#                              label =        Page {page}
#                              anno_id =      {manifest_root_id}/annotation/p{page}-image
#                              anno_page_id = {manifest_root_id}/page/p{page}/1
#                              """)
            
            # On peut maintenant écrire le manifest dans un fichier
            manifest_fichier = f"{dossier_manifest}/{dossier}.json"
            with open(manifest_fichier, "w", encoding="utf-8") as f:
                f.write(manifest.json(indent=2))



except FileNotFoundError:
    print(f"Erreur : Le fichier est introuvable.")
except Exception as e:
    print(f"Erreur inattendue : {e}")

