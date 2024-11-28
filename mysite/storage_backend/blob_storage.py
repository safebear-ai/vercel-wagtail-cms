import requests
import vercel_blob
from django.core.files.base import File
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from mysite.config import AppSettings

config = AppSettings()
print(f"ENVIRONMENT : {config.environment}")
print(f"DATABASE_URL : {config.database_url}")

class VercelBlobStorage(Storage):
    def __init__(self):
        self.token: str = config.blob_read_write_token
        self.base_url: str = "https://gqb3dhg6ajkwelj6.public.blob.vercel-storage.com"
        if not self.token:
            raise Exception("BLOB_READ_WRITE_TOKEN environment variable not set")

    def _save(self, name, content):

        print(f"Uploading {name} to Vercel Blob Store...")
        try:
            # Le contenu doit être un objet de type File ou ContentFile
            if isinstance(content, File):
                content.seek(0)  # S'assurer que le fichier est lu depuis le début
                content_bytes = content.read()  # Lire le fichier sous forme de bytes
            else:
                raise ValueError("[VercelBlobStorage] Le contenu du fichier n'est pas un objet valide de type File.")

            if not isinstance(content_bytes, bytes):
                raise ValueError("[VercelBlobStorage] Le contenu du fichier n'a pas pu être converti en bytes.")

            # Utiliser le SDK Vercel Blob pour uploader le fichier
            response = vercel_blob.put(path=name, data=content_bytes, options={"token": self.token})

            print(f"Response : {response}")
            
            if not response or 'url' not in response:
                raise Exception("[VercelBlobStorage] Erreur lors de l'upload sur Vercel Blob : Réponse invalide.")

            # Retourner l'URL après l'upload réussi
            print(f"Upload réussi : {response['url']}")
            file_name = response['url'].split("/")[-1]
            return file_name

        except Exception as e:
            raise Exception(f"[VercelBlobStorage] Erreur lors de l'upload sur Vercel Blob : {e}")

    def _open(self, name, mode='rb'):
        # Implémentation basique qui évite un conflit, toujours considérer qu'il n'existe pas
        return None

    def delete(self, url):
        try:
            # Utiliser le SDK Vercel Blob pour supprimer le fichier
            response = vercel_blob.delete(url=url, options={"token": self.token})
            print(response)
            print(f"Suppression de l'image dans le Blob Store : {url}")
        except Exception as e:
            raise Exception(f"[VercelBlobStorage] Erreur lors de la suppression sur Vercel Blob : {e}")
            

    def exists(self, name):
        # Implémentation basique qui évite un conflit, toujours considérer qu'il n'existe pas
        return False

    def url(self, pathname):
        # Retourner l'URL du fichier
        print(f"Retourner l'URL du fichier : {pathname} ======> {self.base_url}/{pathname}")
        return f"{self.base_url}/{pathname}"