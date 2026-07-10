from django.urls import path
from loja.views.CategoriaView import list_categoria_view, create_categoria_view, edit_categoria_view, delete_categoria_view

urlpatterns = [
    path('', list_categoria_view, name='list_categoria'),
    path('novo/', create_categoria_view, name='create_categoria'),
    path('editar/<int:id>/', edit_categoria_view, name='edit_categoria'),
    path('deletar/<int:id>/', delete_categoria_view, name='delete_categoria'),
]