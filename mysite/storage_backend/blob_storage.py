import os
import vercel_blob
from django.core.files.storage import Storage
from django.core.files.base import File

class VercelBlobStorage(Storage):
    def __init__(self):
        super().__init__()

    def _save(self, name, content):
        # Utiliser le SDK pour télécharger le fichier sur Vercel Blob
        try:
            result = vercel_blob.put(name, content, options={"access": "public"})
            return result.get("url")
        except Exception as e:
            raise Exception(f"Erreur lors de l'upload sur Vercel Blob : {e}")

    def url(self, name):
        # Générer l'URL publique à partir du nom du fichier
        return f"https://vercel.blob.store/{name}"

    def exists(self, name):
        # Vercel Blob ne permet pas facilement de vérifier l'existence du fichier
        return False