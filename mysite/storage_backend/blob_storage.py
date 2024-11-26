import vercel_blob
from django.core.files.base import File
from django.core.files.storage import Storage
from mysite.config import AppSettings


config = AppSettings()
print(f"ENVIRONMENT : {config.environment}")
print(f"DATABASE_URL : {config.database_url}")

class VercelBlobStorage(Storage):
    def __init__(self):
        self.token = config.blob_read_write_token
        if not self.token:
            raise Exception("BLOB_READ_WRITE_TOKEN environment variable not set")
        self.base_url = config.api_base_url

    def _save(self, name, content):
        try:
            # Vérifier que le contenu est bien un fichier et lire les données
            if isinstance(content, File):
                content.seek(0)  # Assurez-vous de commencer la lecture au début
                file_data = content.read()
                
                print(file_data)
            else:
                raise ValueError("Le contenu fourni n'est pas un fichier valide.")

            # Utiliser le SDK Vercel Blob pour uploader le fichier
            response = vercel_blob.put(name, file_data)
            
            print(response)

            # Vérification de la réponse de Vercel Blob
            if not response or 'url' not in response:
                raise Exception(f"Erreur lors de l'upload : aucune URL retournée - {response}")

            # Afficher l'URL en cas de succès (optionnel, uniquement pour déboguer)
            print(response.get('url'))

            # Retourner l'URL après l'upload réussi
            return response.get('url')

        except Exception as e:
            raise Exception(f"Erreur lors de l'upload sur Vercel Blob : {e}")

    def exists(self, name):
        # Implémentation pour évite un conflit
        return False

    def url(self, name):
        return f"{self.base_url}/{name}"  # Retourner l'URL publique si nécessaire