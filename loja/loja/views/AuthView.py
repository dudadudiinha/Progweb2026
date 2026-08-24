from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from loja.forms.AuthForm import LoginForm, RegisterForm

def login_view(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Redirecionamento com o parâmetro 'next'
                _next = request.GET.get('next')
                if _next is not None:
                    return redirect(_next)
                else:
                    return redirect("/")
            else:
                context = {
                    'form': loginForm,
                    'msg': 'Usuário ou senha inválidos'
                }
                return render(request, 'auth/login.html', context=context)
    else:
        loginForm = LoginForm()
        
    return render(request, 'auth/login.html', {'form': loginForm})

def register_view(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            return redirect('/login')
    else:
        registerForm = RegisterForm()
        
    return render(request, 'auth/register.html', {'form': registerForm})

def logout_view(request):
    logout(request)
    return redirect('/login')