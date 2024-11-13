"""
Custom overrides of Wagtail Document and Image models. All other
models related to website content should most likely go in
``website.models`` instead.
"""

from django.db import models
from wagtail.documents.models import AbstractDocument
from wagtail.documents.models import Document
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images import get_image_model_string
import os
import requests
from django.conf import settings
import vercel_blob

BLOB_READ_WRITE_TOKEN = os.getenv(
    "BLOB_READ_WRITE_TOKEN",
    "vercel_blob_rw_gQb3DHG6aJKWElj6_A1CzC7NbP3Asf3I6t5Zccj8mWPXfpS",
)
VERCEL_BLOB_API_URL = "https://api.vercel.com/v1/blobs"


class CustomImage(AbstractImage):
    blob_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Vérifier si l'image a déjà été uploadée
        if not self.blob_url:
            with self.file.open("rb") as f:
                # Lire le contenu du fichier
                file_content = f.read()
                # Définir le nom du fichier
                file_name = self.file.name

                # Upload vers le Blob Store de Vercel
                try:
                    response = vercel_blob.put(
                        file_name, file_content, {"access": "public"}
                    )
                    self.blob_url = response.get("url")
                except Exception as e:
                    raise Exception(
                        f"Erreur lors de l'upload sur Vercel Blob Store : {e}"
                    )

        # Appel de la méthode save() du parent pour enregistrer l'objet
        super().save(*args, **kwargs)

    admin_form_fields = Image.admin_form_fields + ("blob_url",)


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
