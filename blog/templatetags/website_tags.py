from django import template

from safebear_cms.models import Footer
from safebear_cms.models import Navbar


register = template.Library()


@register.simple_tag
def get_safebear_cms_navbars():
    # NOTE: For a multi-site, you may need to create SiteSettings to
    # choose a Navbar, then query those here. Or, add a Foreign Key to
    # the Site on the Navbar, and query those.
    return Navbar.objects.all()


@register.simple_tag
def get_safebear_cms_footers():
    # NOTE: For a multi-site, you may need to create SiteSettings to
    # choose a Footer, then query those here. Or, add a Foreign Key to
    # the Site on the Footer, and query those.
    return Footer.objects.all()