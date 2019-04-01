from django.contrib import admin
from .models import PureSite, Attribut, TypeElement, Element, Page

admin.site.register(PureSite)
admin.site.register(Attribut)
admin.site.register(TypeElement)
admin.site.register(Element)
admin.site.register(Page)
