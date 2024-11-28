import os
import requests
import vercel_blob
from django.core.files.base import File
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from mysite.config import AppSettings

config = AppSettings()
print(f"ENVIRONMENT : {config.environment}")
print(f"DATABASE_URL : {config.database_url}")

class VercelBlobStore(Storage):
    """
    Custom Django Storage backend for Vercel Blob Store.
    """
    def __init__(self, vercel_token=None, blob_base_url=None):
        self.vercel_token = vercel_token or os.getenv("BLOB_READ_WRITE_TOKEN")
        self.blob_base_url = blob_base_url or "https://api.vercel.com/v2/now/blobs"
        if not self.vercel_token:
            raise ValueError("Vercel token must be provided either via parameter or environment variable VERCEL_BLOB_TOKEN")

    def _open(self, name, mode='rb'):
        """Retrieve the specified file from storage."""
        response = requests.get(f"{self.blob_base_url}/{name}", headers=self._get_headers())
        if response.status_code != 200:
            raise FileNotFoundError(f"File '{name}' not found in Vercel Blob Store.")
        return File(response.content)

    def _save(self, name, content):
        """Save new content to the file specified by name."""
        headers = self._get_headers()
        files = {'file': (name, content)}
        response = requests.post(self.blob_base_url, headers=headers, files=files)
        if response.status_code != 200:
            raise IOError(f"Failed to upload file to Vercel Blob Store: {response.content}")
        return name

    def delete(self, name):
        """Delete the specified file from the storage system."""
        response = requests.delete(f"{self.blob_base_url}/{name}", headers=self._get_headers())
        if response.status_code != 200:
            raise FileNotFoundError(f"Failed to delete '{name}' from Vercel Blob Store.")

    def exists(self, name):
        """Return True if a file referenced by the given name already exists in the storage system."""
        response = requests.head(f"{self.blob_base_url}/{name}", headers=self._get_headers())
        return response.status_code == 200

    def listdir(self, path):
        """List the contents of the specified path."""
        response = requests.get(self.blob_base_url, headers=self._get_headers())
        if response.status_code != 200:
            raise IOError("Failed to list directory in Vercel Blob Store.")
        data = response.json()
        files = data.get("files", [])
        return [], files

    def size(self, name):
        """Return the total size, in bytes, of the file specified by name."""
        response = requests.head(f"{self.blob_base_url}/{name}", headers=self._get_headers())
        if response.status_code != 200:
            raise FileNotFoundError(f"File '{name}' not found in Vercel Blob Store.")
        return int(response.headers.get('Content-Length', 0))

    def url(self, name):
        """Return an absolute URL where the file's contents can be accessed directly by a web browser."""
        return f"{self.blob_base_url}/{name}"

    def get_accessed_time(self, name):
        raise NotImplementedError("Vercel Blob Store does not support accessed time.")

    def get_created_time(self, name):
        raise NotImplementedError("Vercel Blob Store does not support created time.")

    def get_modified_time(self, name):
        raise NotImplementedError("Vercel Blob Store does not support modified time.")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.vercel_token}"
        }

    def get_available_name(self, name, max_length=None):
        """Return a filename that's free on the target storage system and available for new content to be written to."""
        name = str(name).replace("\\", "/")
        dir_name, file_name = os.path.split(name)
        if ".." in pathlib.PurePath(dir_name).parts:
            raise SuspiciousFileOperation(
                "Detected path traversal attempt in '%s'" % dir_name
            )
        file_root, file_ext = os.path.splitext(file_name)
        while self.exists(name):
            name = os.path.join(
                dir_name, "%s_%s%s" % (file_root, get_random_string(7), file_ext)
            )
            if max_length and len(name) > max_length:
                raise SuspiciousFileOperation(
                    'Storage can not find an available filename for "%s". '
                    "Please make sure that the corresponding file field "
                    'allows sufficient "max_length".' % name
                )
        return name