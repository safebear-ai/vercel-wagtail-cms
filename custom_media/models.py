"""
Custom overrides of Wagtail Document and Image models. All other
models related to website content should most likely go in
``website.models`` instead.
"""
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv()
import os
import tempfile

import vercel_blob
from django.core.files.storage import default_storage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.models import AbstractDocument
from wagtail.images.models import AbstractImage, AbstractRendition, Image

from mysite.config import AppSettings

config = AppSettings()

BLOB_READ_WRITE_TOKEN: str = config.blob_read_write_token

VERCEL_BLOB_API_URL: str = "https://api.vercel.com/v1/blobs"



class CustomImage(AbstractImage):
    blob_url = models.URLField(blank=True, null=True)
    admin_form_fields = Image.admin_form_fields + (
        'blob_url',
    )

    def save(self, *args, **kwargs):
        """
        Saves the CustomImage instance, uploading the file to Vercel's Blob Store
        if it has not already been uploaded.

        This method checks if the image has a blob_url. If not, it uploads the image content
        using the default storage backend (which should be VercelBlobStorage).
        """
        if not self.blob_url:
            # Utiliser le backend de stockage par défaut pour sauvegarder l'image
            try:
                file_name = self.file.name
                self.blob_url = default_storage.save(file_name, self.file)
            except Exception as e:
                raise Exception(f"Erreur lors de l'upload sur Vercel Blob Store : {e}")

        # Sauvegarder dans la base de données
        super().save(*args, **kwargs)
    
    @property
    def get_image_url(self):
        """
        Override the default file URL to use blob_url.
        """
        return self.blob_url or super().file.url

    def delete(self, *args, **kwargs):
        """
        Surcharge de la méthode delete pour supprimer l'image du Blob Store
        avant de la retirer de la base de données.
        """
        try:
            if self.blob_url:
                default_storage.delete(self.blob_url)
        except Exception as e:
            print(f"Erreur lors de la suppression de l'image dans le Blob Store : {e}")

        # Supprimer l'entrée de la base de données
        super().delete(*args, **kwargs)
        
    @property
    def get_image_url(self):
        """
        Override the default file URL to use blob_url.
        """
        return self.blob_url or super().file.url
    
    def delete(self, *args, **kwargs):
        """
        Surcharge de la méthode delete pour supprimer l'image du Blob Store
        avant de la retirer de la base de données.
        """
        try:
            # Delete from Blob Store if blob_url is defined
            if self.blob_url:
                response = vercel_blob.delete(self.blob_url)
                if response.get("status") != "success":
                    raise Exception(f"Erreur lors de la suppression dans le Blob Store : {response}")
        except Exception as e:
            print(f"Erreur lors de la suppression de l'image dans le Blob Store : {e}")

        # Delete entry from database
        super().delete(*args, **kwargs)
        


class CustomImageTag(models.Model):
    tag = models.ForeignKey(
        "taggit.Tag",
        related_name="custom_media_image_tags",  # Change related_name to make it unique
        on_delete=models.CASCADE,
    )
    content_object = models.ForeignKey(
        CustomImage,
        related_name="custom_media_tagged_items",  # Change related_name to make it unique
        on_delete=models.CASCADE,
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class CustomDocument(AbstractDocument):
    # Ajoutez des champs personnalisés ici si nécessaire
    extra_info = models.TextField(blank=True, null=True)

    # admin_form_fields = AbstractDocument.admin_form_fields + ('extra_info',)
