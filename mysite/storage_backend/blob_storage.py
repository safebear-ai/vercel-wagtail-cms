import vercel_blob
from django.core.files.base import File
from django.core.files.storage import FileSystemStorage, Storage

from mysite.config import AppSettings

config = AppSettings()
print(f"ENVIRONMENT : {config.environment}")
print(f"DATABASE_URL : {config.database_url}")

class VercelBlobStorage(Storage):
    def __init__(self):
        self.token: str = config.blob_read_write_token
        if not self.token:
            raise Exception("BLOB_READ_WRITE_TOKEN environment variable not set")
        self.base_url: str = config.api_base_url

    def _save(self, name, content):
        print(f"Uploading {name} to Vercel Blob Store...")
        try:
            # Utiliser le SDK Vercel Blob pour uploader le fichier
            response = vercel_blob.put(path=name, data=content)
            print(response)
            if not response or 'url' not in response:
                raise Exception("Erreur lors de l'upload sur Vercel Blob : Réponse invalide.")

            # Retourner l'URL après l'upload réussi
            print(f"Upload réussi : {response['url']}")
            return response['url']

        except Exception as e:
            raise Exception(f"Erreur lors de l'upload sur Vercel Blob : {e}")


    def exists(self, name):
        # Implémentation basique qui évite un conflit, toujours considérer qu'il n'existe pas
        return False

    def url(self, name):
        # Retourner l'URL du fichier
        return f"https://vercel.blob.store/{name}"