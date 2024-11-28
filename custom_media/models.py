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
    blob_url = models.URLField(max_length=500,blank=True, null=True)
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
            # Use the default storage backend to save the image
            try:
                file_name = self.file.name
                if isinstance(self.file, File):
                    try:
                        self.file.seek(0)  # Make sure the file is read from the beginning
                        content = self.file.read()
                
                        # Check if the content is a bytes object
                        if not isinstance(content, bytes):
                            raise ValueError("Le contenu du fichier n'a pas pu être converti en bytes.")
                        
                        # Create a ContentFile object from bytes for storage
                        content_file = ContentFile(content)

                    except Exception as e:
                        raise Exception(f"Erreur lors de la lecture du fichier : {e}")
                else:
                    raise ValueError("Le fichier n'est pas valide.")
                    
                # Call default_storage to upload image and retrieve stored file name
                upload_result: str = default_storage.save(file_name, content_file)

                # Call to default_storage.url to obtain the full URL of the stored image
                self.blob_url: str = default_storage.url(upload_result)

            except Exception as e:
                raise Exception(f"[CustomImage] Erreur lors de l'upload sur Vercel Blob Store : {e}")

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
                print(f"Suppression de l'image dans le Blob Store : {self.blob_url}")
                default_storage.delete(self.blob_url)
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

    # 
    def save(self, *args, **kwargs):
        # Added method for updating rendition URLs after CustomImage update
        if self.image.blob_url:
            self.blob_url = self.image.blob_url
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class CustomDocument(AbstractDocument):
    # Ajoutez des champs personnalisés ici si nécessaire
    extra_info = models.TextField(blank=True, null=True)

    # admin_form_fields = AbstractDocument.admin_form_fields + ('extra_info',)
