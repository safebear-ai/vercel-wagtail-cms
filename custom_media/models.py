"""
Custom overrides of Wagtail Document and Image models. All other
models related to website content should most likely go in
``website.models`` instead.
"""
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.db import models
from wagtail.documents.models import AbstractDocument
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from django.core.files.base import ContentFile
from mysite.config import AppSettings

config = AppSettings()

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
                if isinstance(self.file, File):
                    self.file.seek(0)  # S'assurer que le fichier est lu depuis le début
                    content = ContentFile(self.file.read())  # Convertir le contenu en ContentFile

                # Appel à default_storage pour uploader l'image et récupérer le nom du fichier stocké
                stored_name = default_storage.save(file_name, content)

                # Appel à default_storage.url pour obtenir l'URL complète de l'image stockée
                self.blob_url = default_storage.url(stored_name)
                
                print(f"Image uploaded to Vercel Blob Store : {self.blob_url}")

            except Exception as e:
                raise Exception(f"Erreur lors de l'upload sur Vercel Blob Store : {e}")

        # Sauvegarder dans la base de données
        super().save(*args, **kwargs)

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
