from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_site/', views.create_site, name='create_site'),
    path('edit_site/<int:id_pure_site>/', views.edit_site, name='edit_site'),
    path('edit_site/<int:id_pure_site>/create_page/', views.create_page, name='create_page'),
    path('edit_page/<int:id_page>/', views.edit_page, name='edit_page'),
    path('add_element/<int:id_elem>/to/<int:id_page>/', views.add_element),
    path('remove_element/<int:id_elem>/', views.remove_element),
    path('get_attributs/<int:id_elem>/', views.get_attributs),
    path('update_element/<int:id_elem>/', views.update_attributs),
    path('get_html/<int:id_page>/', views.get_html),
]
