from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm

def list_usuario_view(request, id=None):
    usuarios = Usuario.objects.filter(perfil=2)
    context = {
        'usuarios': usuarios
    }
    return render(request, template_name='usuario/usuario.html', context=context, status=200)


@login_required(login_url='/admin/')
def edit_usuario_view(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    user_instance = usuario.user
    
    message = None

    if request.method == 'POST':
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario)
        userForm = UserForm(request.POST, instance=user_instance)

        if usuarioForm.is_valid() and userForm.is_valid():
            usuarioForm.save()
            userForm.save()
            message = {'type': 'success', 'text': 'Dados atualizados com sucesso'}
        else:
            message = {'type': 'danger', 'text': 'Dados inválidos'}
    else:
        usuarioForm = UserUsuarioForm(instance=usuario)
        userForm = UserForm(instance=user_instance)

    context = {
        'usuarioForm': usuarioForm,
        'userForm': userForm,
        'message': message
    }
    
    return render(request, template_name='usuario/usuario-edit.html', context=context, status=200)