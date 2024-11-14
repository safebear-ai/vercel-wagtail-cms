from wagtail import hooks
from . import models

@hooks.register("construct_image_chooser_queryset")
def include_blob_url_in_chooser_queryset(queryset, request):
    """
    Ajoute le champ blob_url dans les requêtes de l'admin panel.
    """
    return queryset.annotate(blob_url=models.F("blob_url"))
