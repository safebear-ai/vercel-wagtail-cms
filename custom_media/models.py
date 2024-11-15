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
import tempfile
import vercel_blob
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
        # Vérifiez si l'image a déjà été uploadée
        if not self.blob_url:
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(dir='/tmp', delete=False) as tmp_file:
                self.file.seek(0)  # S'assurer que le fichier est lu depuis le début
                tmp_file.write(self.file.read())
                tmp_file.flush()  # Forcer l'écriture sur le disque

                # Charger le contenu pour l'upload
                with open(tmp_file.name, 'rb') as f:
                    file_content = f.read()
                    file_name = self.file.name

                    # Upload vers le Blob Store de Vercel
                    try:
                        response = vercel_blob.put(file_name, file_content, {"access": "public"})
                        self.blob_url = response.get("url")
                    except Exception as e:
                        raise Exception(f"Erreur lors de l'upload sur Vercel Blob Store : {e}")
                    finally:
                        # Supprimer le fichier temporaire
                        os.remove(tmp_file.name)

        # Sauvegarder dans la base de données
        super().save(*args, **kwargs)
        
    @property
    def url(self):
        """
        Override the default file URL to use blob_url.
        """
        return self.blob_url or super().file.url


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
