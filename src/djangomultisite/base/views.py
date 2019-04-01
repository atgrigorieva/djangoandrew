import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_protect

from .models import PureSite, Page, TypeElement, Element
from .form import SiteForm, PageForm


@login_required
def index(request):
    return render(request, 'base/index.html', {
        'pure_sites': PureSite.objects.filter(master=request.user)
    })


@login_required
def create_site(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site = form.save()
            pure_site = PureSite(
                site=site,
                master=request.user,
                domain=site.domain,
                name=site.name
            )
            pure_site.save()
            return HttpResponseRedirect(
                reverse('edit_site', kwargs={'id_pure_site': pure_site.pk})
            )
    else:
        form = SiteForm()

    return render(request, 'base/create_site.html', {'form': form})


@login_required
def edit_site(request, id_pure_site):
    pure_site = PureSite.objects.get(pk=id_pure_site)
    pages = Page.objects.filter(site=pure_site)

    return render(
        request,
        'base/edit_site.html',
        {'pages': pages, 'pure_site': pure_site}
    )


@login_required
def create_page(request, id_pure_site):
    pure_site = PureSite.objects.get(pk=id_pure_site)
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.site = pure_site
            page.save()
            return HttpResponseRedirect(
                reverse('edit_page', kwargs={'id_page': page.pk})
            )
    else:
        form = PageForm()

    return render(
        request,
        'base/create_page.html',
        {'form': form, 'pure_site': pure_site}
    )


@login_required
@csrf_protect
def edit_page(request, id_page):
    page = Page.objects.get(pk=id_page)
    type_elements = TypeElement.objects.all()
    elements = Element.objects.filter(page=page)

    return render(
        request,
        'base/edit_page.html',
        {
            'type_elements': type_elements,
            'elements': elements,
            'page': page
        }
    )


@login_required
def add_element(request, id_elem, id_page):
    data = dict()
    if request.method == "POST":
        page = Page.objects.get(pk=id_page)
        type_element = TypeElement.objects.get(pk=id_elem)
        element = Element(
            elementType=type_element,
            attributeValues='',
            page=page
        )

        element.save()
        data['element'] = model_to_dict(element)
        data['element']['name'] = type_element.name
        data['element']['attributs'] = []

        for attribut in type_element.attributs.all():
            data['element']['attributs'].append(model_to_dict(attribut))
            try:
                values = json.loads(element.attributeValues)

                if attribut.name in values:
                    data['element']['attributs'][-1]['value'] = values[attribut.name]

            except ValueError:
                pass

    return JsonResponse(data)


@login_required
def remove_element(request, id_elem):
    data = dict()
    if request.method == "POST":
        element = Element.objects.get(pk=id_elem)
        element.delete()

    return JsonResponse(data)


@login_required
def get_attributs(request, id_elem):
    data = dict()
    if request.method == "GET":
        element = Element.objects.get(pk=id_elem)

        data['attributs'] = []

        for attribut in element.elementType.attributs.all():
            data['attributs'].append(model_to_dict(attribut))
            try:
                values = json.loads(element.attributeValues)

                if attribut.name in values:
                    data['attributs'][-1]['value'] = values[attribut.name]

            except ValueError:
                pass

    return JsonResponse(data)


@login_required
def update_attributs(request, id_elem):
    data = dict()
    if request.method == "POST":
        element = Element.objects.get(pk=id_elem)

        element.attributeValues = json.dumps(request.POST)
        element.save()

    return JsonResponse(data)


@login_required
def get_html(request, id_page):
    page = Page.objects.get(pk=id_page)
    elements = Element.objects.filter(page=page)
    html = ''

    if request.method == "GET":
        for element in elements:
            html += '<' + element.elementType.tag

            if element.attributeValues:
                attribute_values = json.loads(element.attributeValues)

                style_attributs_str = ''
                other_attributs_str = ''

                for attribute in attribute_values:
                    if attribute_values[attribute] and attribute != 'inner_html':
                        if element.elementType.attributs.get(name=attribute).isStyle:
                            style_attributs_str += '%s: %s;' % (attribute, attribute_values[attribute])
                        else:
                            other_attributs_str += ' %s=%s' % (attribute, attribute_values[attribute])

                if style_attributs_str:
                    html += ' style="%s"' % style_attributs_str

                if other_attributs_str:
                    html += other_attributs_str

            html += ' id=%d >' % element.id
            # TODO различные экранирования от зловредов
            if element.attributeValues and attribute_values['inner_html']:
                html += attribute_values['inner_html']

            if element.elementType.isPairTag:
                html += '</%s>' % element.elementType.tag

    return HttpResponse(html)
