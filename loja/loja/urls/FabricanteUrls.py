from django.urls import path
from loja.views.FabricanteView import list_fabricante_view, create_fabricante_view, edit_fabricante_view, delete_fabricante_view

urlpatterns = [
    path('', list_fabricante_view, name='list_fabricante'),
    path('novo/', create_fabricante_view, name='create_fabricante'),
    path('editar/<int:id>/', edit_fabricante_view, name='edit_fabricante'),
    path('deletar/<int:id>/', delete_fabricante_view, name='delete_fabricante'),
]