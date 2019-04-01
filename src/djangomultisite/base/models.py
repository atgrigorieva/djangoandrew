from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.urls import reverse


class PureSite(Site):
    """class extends the standard model Site"""

    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        parent_link=True
    )
    master = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('edit_site', kwargs={'id_pure_site': self.id})


class Page(models.Model):
    site = models.ForeignKey(PureSite, on_delete=models.CASCADE)
    href = models.CharField(max_length=200, default='index.html')
    title = models.CharField(max_length=100)
    favicon = models.FileField(upload_to='favicons/')
    keywords = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return '%s/%s' % (str(self.site), self.href)


class Attribut(models.Model):
    name = models.CharField(max_length=50)
    hasValue = models.BooleanField(default=True)
    isStyle = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TypeElement(models.Model):
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    isPairTag = models.BooleanField(default=True)
    attributs = models.ManyToManyField(Attribut)

    def __str__(self):
        return self.name


class Element(models.Model):
    elementType = models.ForeignKey(TypeElement, on_delete=models.CASCADE)
    # для json необходима база postgres
    attributeValues = models.TextField()
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
