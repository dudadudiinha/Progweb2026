from django.shortcuts import render, redirect
from loja.models import Produto, Fabricante, Categoria
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    
    context = {
        'produto': produto, 
        'fabricantes': Fabricantes, 
        'categorias': Categorias
    }
    return render(request, template_name='produto/produto-edit.html', context=context, status=200)

def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")
    produtos = Produto.objects.all()
    
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
        
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
        
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
        
    if categoria is not None:
        produtos = produtos.filter(categoria__Categoria=categoria)
        
    if fabricante is not None:
        produtos = produtos.filter(fabricante__Fabricante=fabricante)
        
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days=int(dias))
        produtos = produtos.filter(criado_em__gte=now)
        
    if id is not None:
        produtos = produtos.filter(id=id)
        
    print(produtos)
    context = {
        'produtos': produtos
    }
    
    return render(request, template_name='produto/produto.html', context=context, status=200)

def edit_produto_postback(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        
        print("postback")
        print(id)
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        print("Categoria ID selecionada:", categoria_id)
        print("Fabricante ID selecionado:", fabricante_id)
        
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            if obj_produto:
                obj_produto.Produto = produto
                obj_produto.destaque = (destaque is not None)
                obj_produto.promocao = (promocao is not None)
                if msgPromocao is not None:
                    obj_produto.msgPromocao = msgPromocao
                obj_produto.categoria = Categoria.objects.filter(id=categoria_id).first()
                obj_produto.fabricante = Fabricante.objects.filter(id=fabricante_id).first()
                obj_produto.alterado_em = timezone.now()
                obj_produto.save()
                print("Produto %s alterado com sucesso!" % produto)
                
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def details_produto_view(request, id=None):
    produtos = Produto.objects.all()

    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    context = {
        'produto': produto
    }
    
    return render(request, template_name='produto/produto-details.html', context=context, status=200)

def delete_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
        
    produto = produtos.first()
    print(produto)
    context = {
        'produto': produto
    }
    return render(request, template_name='produto/produto-delete.html', context=context, status=200)

def delete_produto_postback(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        print("postback-delete")
        print(id)

        try:
            obj_produto = Produto.objects.filter(id=id).first()
            if obj_produto:
                if obj_produto.image:
                    obj_produto.image.delete(save=False)
                obj_produto.delete()
                print("Produto %s e sua imagem foram excluídos com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def create_produto_view(request, id=None):
    if request.method == 'POST':
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        categoria_id = request.POST.get("CategoriaFk")
        fabricante_id = request.POST.get("FabricanteFk")
        
        try:
            obj_produto = Produto()
            obj_produto.Produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
                
            obj_produto.preco = 0
            if (preco is not None) and (preco != ""):
                preco = preco.replace(',', '.')
                obj_produto.preco = preco
                
            obj_produto.categoria = Categoria.objects.filter(id=categoria_id).first()
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante_id).first()
            
            obj_produto.criado_em = timezone.now()
            obj_produto.alterado_em = obj_produto.criado_em
            if request.FILES and 'image' in request.FILES:
                obj_produto.image = request.FILES['image']
            
            obj_produto.save()
            print("Produto %s inserido com sucesso!" % produto)
            return redirect("/produto")
            
        except Exception as e:
            print("ERRO REAL AO INSERIR PRODUTO: %s" % e)
            return redirect("/produto")
            
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    context = {
        'fabricantes': Fabricantes,
        'categorias': Categorias
    }
    return render(request, template_name='produto/produto-create.html', context=context, status=200)