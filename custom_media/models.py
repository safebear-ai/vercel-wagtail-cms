"""
Custom overrides of Wagtail Document and Image models. All other
models related to website content should most likely go in
``website.models`` instead.
"""
from dotenv import load_dotenv

# Charge les variables d'environnement
load_dotenv()
from django.db import models
from wagtail.documents.models import AbstractDocument
from wagtail.images.models import Image, AbstractImage, AbstractRendition
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
        # Check if the image has already been uploaded
        """
        Saves the CustomImage instance, uploading the file to Vercel's Blob Store
        if it has not already been uploaded.

        This method checks if the image has a blob_url. If not, it creates a temporary
        file and uploads the image content to Vercel's Blob Store, setting the blob_url
        upon successful upload. After uploading, it removes the temporary file.

        Parameters:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Raises:
        Exception: If an error occurs during the upload to Vercel's Blob Store.
        """
        if not self.blob_url:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(dir='/tmp', delete=False) as tmp_file:
                self.file.seek(0)  # Make sure the file is read from the beginning
                tmp_file.write(self.file.read())
                tmp_file.flush()  # Force write
                
                # Uploading content
                with open(tmp_file.name, 'rb') as f:
                    file_content = f.read()
                    file_name = self.file.name

                    # Upload to Vercel's Blob Store
                    try:
                        response = vercel_blob.put(file_name, file_content, {"access": "public"})
                        self.blob_url = response.get("url")
                    except Exception as e:
                        raise Exception(f"Erreur lors de l'upload sur Vercel Blob Store : {e}")
                    finally:
                        # Delete temporary file
                        os.remove(tmp_file.name)

        # Save to database
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
