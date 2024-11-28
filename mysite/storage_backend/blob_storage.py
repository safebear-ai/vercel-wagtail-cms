import json
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
        self._log_info(f"Début de l'upload de {name} vers Vercel Blob Store...")
        try:
            content_bytes = self._get_content_as_bytes(content)
            response = self._upload_to_vercel_blob(name, content_bytes)
            file_name = self._handle_successful_upload(response)
            return file_name

        except Exception as e:
            self._log_error(f"Erreur lors de l'upload sur Vercel Blob : {e}")
            raise Exception(f"[VercelBlobStorage] Erreur lors de l'upload sur Vercel Blob : {e}")


    def _get_content_as_bytes(self, content):
        if isinstance(content, File):
            self._log_info("Lecture du contenu du fichier...")
            content.seek(0)  # Make sure the file is read from the beginning
            content_bytes = content.read()  # Read file as bytes
        else:
            raise ValueError("[VercelBlobStorage] Le contenu n'est pas un objet valide de type File.")

        if not isinstance(content_bytes, bytes):
            raise ValueError("[VercelBlobStorage] Le contenu du fichier n'a pas pu être converti en bytes.")

        self._log_info("Contenu du fichier converti avec succès en bytes.")
        return content_bytes


    def _upload_to_vercel_blob(self, name, content_bytes):
        self._log_info("Upload du fichier sur Vercel Blob Store...")
        response = vercel_blob.put(path=name, data=content_bytes, options={"token": self.token})
        self._log_debug("Réponse du serveur Vercel :", json.dumps(response, indent=2))

        if not response or "url" not in response:
            raise Exception("[VercelBlobStorage] Erreur lors de l'upload sur Vercel Blob : Réponse invalide.")

        return response


    def _handle_successful_upload(self, response):
        self._log_info(f"Upload réussi : {response['url']}")
        file_name = response["url"].split("/")[-1]
        return file_name


    def _log_info(self, message):
        print(f"[INFO] {message}")


    def _log_error(self, message):
        print(f"[ERREUR] {message}")


    def _log_debug(self, prefix, data):
        print(f"[DEBUG] {prefix} {data}")

    def _open(self, name, mode="rb"):
        """
        Ouvre le fichier spécifié à partir de Vercel Blob Store.
        """
        try:
            # Utiliser la méthode download du SDK pour obtenir le contenu du fichier
            response = vercel_blob.download_file(name)
            if response:
                # Retourner le contenu encapsulé dans un ContentFile pour Django
                return ContentFile(response)
            else:
                raise Exception(
                    f"[VercelBlobStorage] Impossible de télécharger le fichier : {name}"
                )

        except Exception as e:
            raise Exception(
                f"[VercelBlobStorage] Erreur lors de l'ouverture du fichier sur Vercel Blob : {e}"
            )

    def delete(self, name):
        try:
            # Utiliser le SDK Vercel Blob pour supprimer le fichier
            response = vercel_blob.delete(
                url=f"{self.base_url}/{name}", options={"token": self.token}
            )
            print(response)
            print(f"Fichier supprimé sur Vercel Blob : {name}")
        except Exception as e:
            raise Exception(
                f"[VercelBlobStorage] Erreur lors de la suppression sur Vercel Blob : {e}"
            )

    def exists(self, name):
        # Implémentation basique qui évite un conflit, toujours considérer qu'il n'existe pas
        return False

    def url(self, pathname):
        # Retourner l'URL du fichier
        print(
            f"""
            
            Non final du média : {pathname}
            Blob URL du média : {self.base_url}/{pathname}
            
            """
        )
        return f"{self.base_url}/{pathname}"
