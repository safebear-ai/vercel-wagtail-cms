from io import BytesIO
import json
import requests
import vercel_blob
from django.core.files.base import File
from django.core.files.storage import Storage
from safebear_cms.settings.base import MEDIA_URL
from safebear_cms.config import AppSettings

config: AppSettings = AppSettings()
BASE_URL: str = config.blob_base_url
BLOB_READ_WRITE_TOKEN: str = config.blob_read_write_token


class VercelBlobStore(Storage):
    """
    Custom Django Storage backend for Vercel Blob Store
    """

    def __init__(self):
        self.vercel_token = config.blob_read_write_token
        self.blob_base_url = config.blob_base_url
        if not self.vercel_token:
            raise ValueError(
                "Vercel token must be provided either via parameter or environment variable VERCEL_BLOB_TOKEN"
            )

    def _save(self, name, content):
        """Save new content to the file specified by name."""

        content = content.read()
        response = vercel_blob.put(
            path=name, data=content, options={"token": self.vercel_token}
        )

        print(json.dumps(response, indent=4))  # print the response
        original_file_name = response["url"].split("/")[-2]
        print(original_file_name + "/" + response["url"].split("/")[-1])
        return original_file_name + "/" + response["url"].split("/")[-1]

    def _open(self, name, mode="rb"):
        """Retrieve the specified file from storage."""
        print(f"Opening file: {MEDIA_URL}{name}")
        file_url = f"{MEDIA_URL}{name}"
        response = requests.get(file_url)
        if response.status_code != 200:
            raise FileNotFoundError(
                f"Unable to retrieve file '{name}' from Vercel Blob Store."
            )
        return File(BytesIO(response.content), name)

    def delete(self, name):
        """Delete the specified file from the storage system."""
        response = vercel_blob.delete(
            f"{MEDIA_URL}{name}", options={"token": self.vercel_token}
        )
        print(json.dumps(response, indent=4))

    def exists(self, name):
        """Return True if a file referenced by the given name already exists in the storage system."""
        response = requests.head(
            f"{self.blob_base_url}/{name}", headers=self._get_headers()
        )
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
        response = requests.head(
            f"{self.blob_base_url}/{name}", headers=self._get_headers()
        )
        if response.status_code != 200:
            raise FileNotFoundError(f"File '{name}' not found in Vercel Blob Store.")
        return int(response.headers.get("Content-Length", 0))

    def url(self, name):
        # """Return an absolute URL where the file's contents can be accessed directly by a web browser."""
        file_path = f"{MEDIA_URL}{name}"
        print(f"media url: {file_path}")
        # URL pour les documents
        return file_path

    def get_blob_metadata(self, name):
        response = vercel_blob.head(f"{self.blob_base_url}/{name}")
        print(response)
        return response

    def _get_headers(self):
        return {"Authorization": f"Bearer {self.vercel_token}"}
