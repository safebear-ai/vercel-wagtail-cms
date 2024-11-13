"""
Create or customize your page models here.
"""

from coderedcms.blocks import HTML_STREAMBLOCKS
from coderedcms.blocks import LAYOUT_STREAMBLOCKS
from coderedcms.blocks import BaseBlock
from coderedcms.blocks import BaseLinkBlock
from coderedcms.blocks import LinkStructValue
from coderedcms.forms import CoderedFormField
from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEmail
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedFormPage
from coderedcms.models import CoderedLocationIndexPage
from coderedcms.models import CoderedLocationPage
from coderedcms.models import CoderedWebPage
from custom_user import models as custom_user_models
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet

from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images import get_image_model_string
import requests
import os

from django.conf import settings

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

BLOB_READ_WRITE_TOKEN = os.getenv("BLOB_READ_WRITE_TOKEN")
VERCEL_BLOB_API_URL = "https://api.vercel.com/v1/blobs"


class CustomImage(AbstractImage):
    """
    Modèle personnalisé pour l'application `website`.
    """
    blob_url = models.URLField(blank=True, null=True)

    tags = models.ManyToManyField(
        'taggit.Tag',
        through='website.CustomImageTag',
        related_name='website_images',  # Change related_name to make it unique
        blank=True
    )

    uploaded_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name='website_uploaded_images'  # Change related_name to make it unique
    )

    def save(self, *args, **kwargs):
        # Envoi du fichier à l'API Blob de Vercel (comme précédemment expliqué)
        ...

class CustomImageTag(models.Model):
    tag = models.ForeignKey(
        'taggit.Tag',
        related_name='website_image_tags',  # Change related_name to make it unique
        on_delete=models.CASCADE
    )
    content_object = models.ForeignKey(
        CustomImage,
        related_name='website_tagged_items',  # Change related_name to make it unique
        on_delete=models.CASCADE
    )

class CustomRendition(AbstractRendition):
    """
    Classe pour gérer les rendus d'images personnalisés.
    """
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='website_renditions')

    class Meta:
        unique_together = (('image', 'filter_spec', 'focal_point_key'),)

class ArticlePage(CoderedArticlePage):
    """
    Article, suitable for news or blog content.
    """

    class Meta:
        verbose_name = "Article"
        ordering = ["-first_published_at"]

    # Only allow this page to be created beneath an ArticleIndexPage.
    parent_page_types = ["website.ArticleIndexPage"]

    template = "coderedcms/pages/article_page.html"
    search_template = "coderedcms/pages/article_page.search.html"


class ArticleIndexPage(CoderedArticleIndexPage):
    """
    Shows a list of article sub-pages.
    """

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get("tag")
        blogpages = ArticlePage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context

    class Meta:
        verbose_name = "Article Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.ArticlePage"

    # Only allow ArticlePages beneath this page.
    subpage_types = ["website.ArticlePage"]

    template = "coderedcms/pages/article_index_page.html"


class EventPage(CoderedEventPage):
    class Meta:
        verbose_name = "Event Page"

    parent_page_types = ["website.EventIndexPage"]
    template = "coderedcms/pages/event_page.html"


class EventIndexPage(CoderedEventIndexPage):
    """
    Shows a list of event sub-pages.
    """

    class Meta:
        verbose_name = "Events Landing Page"

    index_query_pagemodel = "website.EventPage"

    # Only allow EventPages beneath this page.
    subpage_types = ["website.EventPage"]

    template = "coderedcms/pages/event_index_page.html"


class EventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(EventPage, related_name="occurrences")


class FormPage(CoderedFormPage):
    """
    A page with an html <form>.
    """

    class Meta:
        verbose_name = "Form"

    template = "coderedcms/pages/form_page.html"


class FormPageField(CoderedFormField):
    """
    A field that links to a FormPage.
    """

    class Meta:
        ordering = ["sort_order"]

    page = ParentalKey("FormPage", related_name="form_fields")


class FormConfirmEmail(CoderedEmail):
    """
    Sends a confirmation email after submitting a FormPage.
    """

    page = ParentalKey("FormPage", related_name="confirmation_emails")


class LocationPage(CoderedLocationPage):
    """
    A page that holds a location.  This could be a store, a restaurant, etc.
    """

    class Meta:
        verbose_name = "Location Page"

    template = "coderedcms/pages/location_page.html"

    # Only allow LocationIndexPages above this page.
    parent_page_types = ["website.LocationIndexPage"]


class LocationIndexPage(CoderedLocationIndexPage):
    """
    A page that holds a list of locations and displays them with a Google Map.
    This does require a Google Maps API Key in Settings > CRX Settings
    """

    class Meta:
        verbose_name = "Location Landing Page"

    # Override to specify custom index ordering choice/default.
    index_query_pagemodel = "website.LocationPage"

    # Only allow LocationPages beneath this page.
    subpage_types = ["website.LocationPage"]

    template = "coderedcms/pages/location_index_page.html"


class WebPage(CoderedWebPage):
    """
    General use page with featureful streamfield and SEO attributes.
    """

    class Meta:
        verbose_name = "Web Page"

    template = "coderedcms/pages/web_page.html"


# -- Navbar & Footer ----------------------------------------------------------


class NavbarLinkBlock(BaseLinkBlock):
    """
    Simple link in the navbar.
    """

    class Meta:
        icon = "link"
        label = "Link"
        template = "website/blocks/navbar_link.html"
        value_class = LinkStructValue


class NavbarDropdownBlock(BaseBlock):
    """
    Custom dropdown menu with heading, links, and rich content.
    """

    class Meta:
        icon = "arrow-down"
        label = "Dropdown"
        template = "website/blocks/navbar_dropdown.html"

    title = blocks.CharBlock(
        max_length=255,
        required=True,
        label="Title",
    )
    links = blocks.StreamBlock(
        [("link", NavbarLinkBlock())],
        required=True,
        label="Links",
    )
    description = blocks.StreamBlock(
        HTML_STREAMBLOCKS,
        required=False,
        label="Description",
    )


@register_snippet
class Navbar(models.Model):
    """
    Custom navigation bar / menu.
    """

    class Meta:
        verbose_name = "Navigation Bar"

    name = models.CharField(
        max_length=255,
    )
    content = StreamField(
        [
            ("link", NavbarLinkBlock()),
            ("dropdown", NavbarDropdownBlock()),
        ],
        use_json_field=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("content"),
    ]

    def __str__(self) -> str:
        return self.name


@register_snippet
class Footer(models.Model):
    """
    Custom footer for bottom of pages on the site.
    """

    class Meta:
        verbose_name = "Footer"

    name = models.CharField(
        max_length=255,
    )
    content = StreamField(
        LAYOUT_STREAMBLOCKS,
        verbose_name="Content",
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("content"),
    ]

    def __str__(self) -> str:
        return self.name
