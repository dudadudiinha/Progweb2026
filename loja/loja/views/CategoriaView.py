from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from loja.models import Categoria

@login_required(login_url='/admin/')
def list_categoria_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/categoria-list.html', {'categorias': categorias})

@login_required(login_url='/admin/')
def create_categoria_view(request):
    message = None
    if request.method == 'POST':
        nome = request.POST.get('Nome')
        if nome:
            Categoria.objects.create(Categoria=nome)
            return redirect('list_categoria')
        else:
            message = {'type': 'danger', 'text': 'O campo nome é obrigatório.'}
    
    return render(request, 'categoria/categoria-form.html', {'message': message})

@login_required(login_url='/admin/')
def edit_categoria_view(request, id=None):
    if request.method == 'POST':
        id_post = request.POST.get("id")
        id_final = id_post if id_post else id
        nome_categoria = request.POST.get("Categoria")
        
        try:
            obj_categoria = Categoria.objects.filter(id=id_final).first()
            if obj_categoria:
                obj_categoria.Categoria = nome_categoria
                obj_categoria.save()
                print("Categoria %s alterada com sucesso!" % nome_categoria)
            else:
                print("Erro: Categoria não encontrada.")
        except Exception as e:
            print("Erro salvando categoria: %s" % e)
        return redirect("/categoria")
    categoria = Categoria.objects.filter(id=id).first()
    if not categoria:
        return redirect('/categoria')
        
    return render(request, 'categoria/categoria-edit.html', {'categoria': categoria})

@login_required(login_url='/admin/')
def delete_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('list_categoria')
    return render(request, 'categoria/categoria-confirm-delete.html', {'categoria': categoria})