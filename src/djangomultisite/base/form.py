from django.forms import ModelForm
from django.contrib.sites.models import Site
from .models import Page


class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ['domain', 'name']


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['href', 'title', 'favicon', 'keywords', 'description']
