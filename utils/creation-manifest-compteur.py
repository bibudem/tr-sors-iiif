# Création d'un squelette de manifest depuis un ID, un nombre
# de pages et le serveur d'images IIIF
import os
import sys
from iiif_prezi3 import Manifest, config

# Quelques variables utiles
iiif_server_base_url = "https://pvj5vvaturp6mtjbgb55ug76eq0fokec.lambda-url.ca-central-1.on.aws/iiif/3/"
manifest_base_id = "https://bibudem.github.io/tresors-iiif/manifests/"
dossier_manifest = "manifests-auto"

if len(sys.argv) != 3:
    print("Usage : python creation-manifest-compteur.py <manifest id> <nombre de pages>")
else:
    id = sys.argv[1]
    nbPage = int(sys.argv[2])

    # On va créer un nouveau manifest
    manifest_root_id = f"{manifest_base_id}{id}"
    manifest_id = f"{manifest_root_id}.json"
    print(f"ID du Manifest = {manifest_id}")
    manifest = Manifest(id=manifest_id, label={"fr": [id]})

    # On va boucler sur les pages
    for i in range(1, nbPage + 1):
        page = f"{i:03}"
        print(f"Page {page}")
        manifest.make_canvas_from_iiif(
            url = f"{iiif_server_base_url}{id}_p{page}",
            id = f"{manifest_root_id}/canvas/p{page}",
            label = f"Page {page}",
            anno_id = f"{manifest_root_id}/annotation/p{page}-image",
            anno_page_id = f"{manifest_root_id}/page/p{page}/1"
        )

    # On peut maintenant écrire le manifest dans un fichier
    manifest_fichier = f"{dossier_manifest}/{id}.json"
    with open(manifest_fichier, "w", encoding="utf-8") as f:
        f.write(manifest.json(indent=2))

