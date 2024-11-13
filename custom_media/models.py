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

BLOB_READ_WRITE_TOKEN = os.getenv('BLOB_READ_WRITE_TOKEN', 'vercel_blob_rw_gQb3DHG6aJKWElj6_A1CzC7NbP3Asf3I6t5Zccj8mWPXfpS')
VERCEL_BLOB_API_URL = "https://api.vercel.com/v1/blobs"

class CustomImage(AbstractImage):
    """
    Modèle personnalisé pour gérer l'upload d'image en utilisant le Blob Store de Vercel.
    """
    blob_url = models.URLField(blank=True, null=True)

    tags = models.ManyToManyField(
        'taggit.Tag',
        through='custom_media.CustomImageTag',
        related_name='custom_media_images',  # Change related_name to make it unique
        blank=True
    )

    uploaded_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name='custom_media_uploaded_images'  # Change related_name to make it unique
    )

    def save(self, *args, **kwargs):
        # Sauvegarde de base pour que le fichier soit accessible
        super().save(*args, **kwargs)

        # Envoi du fichier à l'API Blob de Vercel
        with self.file.open('rb') as f:
            files = {'file': (self.file.name, f, self.file.file.content_type)}
            headers = {
                'Authorization': f'Bearer {BLOB_READ_WRITE_TOKEN}'
            }

            response = requests.post(VERCEL_BLOB_API_URL, headers=headers, files=files)

            if response.status_code == 200:
                blob_data = response.json()
                self.blob_url = blob_data.get("url")
                # Sauvegarder de nouveau l'URL du blob
                super().save(*args, **kwargs)
            else:
                raise Exception(f"Erreur lors de l'upload sur Vercel Blob Store: {response.status_code} {response.text}")

    # admin_form_fields = AbstractImage.admin_form_fields + ('blob_url',)

class CustomImageTag(models.Model):
    tag = models.ForeignKey(
        'taggit.Tag',
        related_name='custom_media_image_tags',  # Change related_name to make it unique
        on_delete=models.CASCADE
    )
    content_object = models.ForeignKey(
        CustomImage,
        related_name='custom_media_tagged_items',  # Change related_name to make it unique
        on_delete=models.CASCADE
    )

class CustomRendition(AbstractRendition):
    """
    Classe pour gérer les rendus d'images personnalisés.
    """
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (('image', 'filter_spec', 'focal_point_key'),)

class CustomDocument(AbstractDocument):
    # Ajoutez des champs personnalisés ici si nécessaire
    extra_info = models.TextField(blank=True, null=True)

    # admin_form_fields = AbstractDocument.admin_form_fields + ('extra_info',)