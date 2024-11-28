from wagtail import hooks
from django.db.models import F
from wagtail.images import get_image_model

Image = get_image_model()


@hooks.register("construct_image_chooser_queryset")
def include_url_in_chooser_queryset(queryset, request):
    """
    Ajoute une annotation distincte pour éviter les conflits avec le champ url.
    """
    # Vérifiez que url est un champ valide du modèle
    if hasattr(Image, "url"):
        print("Annotating queryset with custom_url")
        return queryset.annotate(
            custom_url=F("url")
        )  # Utilisez un autre nom pour l'annotation
    print("No url in model")
    return queryset
