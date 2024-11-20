from wagtail import hooks
from django.db.models import F
from wagtail.images import get_image_model

Image = get_image_model()

@hooks.register("construct_image_chooser_queryset")
def include_blob_url_in_chooser_queryset(queryset, request):
    """
    Ajoute une annotation distincte pour éviter les conflits avec le champ blob_url.
    """
    # Vérifiez que blob_url est un champ valide du modèle
    if hasattr(Image, "blob_url"):
        print("Annotating queryset with custom_blob_url")
        return queryset.annotate(custom_blob_url=F("blob_url"))  # Utilisez un autre nom pour l'annotation
    print("No blob_url in model")
    return queryset
