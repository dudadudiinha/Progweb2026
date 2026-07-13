from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from loja.models import Fabricante
from loja.forms.FabricanteForm import FabricanteForm

@login_required(login_url='/admin/')
def list_fabricante_view(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'fabricante/fabricante-list.html', {'fabricantes': fabricantes})

@login_required(login_url='/admin/')
def create_fabricante_view(request):
    message = None
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_fabricante')
        else:
            message = {'type': 'danger', 'text': 'Dados inválidos. Verifique os erros abaixo.'}
    else:
        form = FabricanteForm()
        
    return render(request, 'fabricante/fabricante-form.html', {'form': form, 'message': message})

@login_required(login_url='/admin/')
def edit_fabricante_view(request, id=None):
    if request.method == 'POST':
        id_post = request.POST.get("id")
        id_final = id_post if id_post else id
        nome_fabricante = request.POST.get("Fabricante")
        
        try:
            obj_fabricante = Fabricante.objects.filter(id=id_final).first()
            if obj_fabricante:
                obj_fabricante.Fabricante = nome_fabricante
                obj_fabricante.save()
        except Exception as e:
            print("Erro ao salvar fabricante: %s" % e)
            
        return redirect("/fabricante")
    fabricante = Fabricante.objects.filter(id=id).first()
    if not fabricante:
        return redirect('/fabricante')
    return render(request, 'fabricante/fabricante-edit.html', {'fabricante': fabricante})

@login_required(login_url='/admin/')
def delete_fabricante_view(request, id):
    fabricante = get_object_or_404(Fabricante, pk=id)
    if request.method == 'POST':
        fabricante.delete()
        return redirect('list_fabricante')
    return render(request, 'fabricante/fabricante-confirm-delete.html', {'fabricante': fabricante})