import warnings
from django import forms
import vercel_blob

from vercel_blob import VercelBlob
from django.utils.translation import gettext_lazy as _

from custom_user.models import User
from safebear_cms.config import AppSettings
from safebear_cms.storage_backend.blob_storage import VercelBlobStore

config: AppSettings = AppSettings()


class AvatarPreferencesForm(forms.ModelForm):
    avatar = forms.ImageField(label=_("Upload a profile picture"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_avatar = self.instance.avatar

    def save(self, commit=True):
        if self.cleaned_data.get("avatar"):
            avatar = self.cleaned_data["avatar"]

            # Utilisez VercelBlob pour uploader l'image
            file_name = f"avatar_images/{avatar.name}"

            # Upload de l'image sur Vercel Blob Store
            vercel_blob.put(
                file_name, avatar, options={"token": config.blob_read_write_token}
            )

            # Remplacez l'URL de l'avatar par l'URL du Blob Store
            self.instance.avatar.name = file_name

        # Supprimez l'ancien avatar si un nouveau est uploadé
        if (
            commit
            and self._original_avatar
            and (self._original_avatar != self.cleaned_data["avatar"])
        ):
            try:
                self._original_avatar.storage.delete(self._original_avatar.name)
            except OSError:
                warnings.warn(
                    "Failed to delete old avatar file: %s" % self._original_avatar.name
                )

        # Appelez la méthode `save()` parente pour sauvegarder le profil utilisateur avec le nouvel avatar
        return super().save(commit=commit)

    class Meta:
        model = User
        fields = ["avatar"]
