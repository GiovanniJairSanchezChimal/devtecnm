from django.shortcuts import render, redirect
from .forms import ProductoForm, ClienteForm, PedidoForm, CategoriaForm, PedidoProductoForm
from .models import Producto, PedidoProducto, Talla
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse

def is_superuser(user):
    return user.is_superuser

@login_required
def registro_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_productos')
    else:
        form = ProductoForm()
    return render(request, 'registro_productos.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def registro_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_clientes')  # Asegúrate de tener una vista y URL para listar clientes
    else:
        form = ClienteForm()
    return render(request, 'registro_clientes.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Crear el pedido
            pedido = form.save()

            # Obtener los productos y las tallas seleccionadas
            productos = request.POST.getlist('productos')  # Lista de productos
            tallas = request.POST.getlist('tallas')  # Lista de tallas

            # Verificar que las listas de productos y tallas tengan la misma longitud
            if len(productos) != len(tallas):
                return HttpResponse("Error: la cantidad de productos y tallas no coincide", status=400)

            # Asociar cada producto con su respectiva talla
            for producto_id, talla in zip(productos, tallas):
                producto = Producto.objects.get(id=producto_id)
                talla_obj, created = Talla.objects.get_or_create(talla=talla)
                PedidoProducto.objects.create(pedido=pedido, producto=producto, talla=talla_obj)

            # Redirigir a una página de éxito o al detalle del pedido
            return redirect('detalle_pedido', pedido_id=pedido.id)  # Redirige al detalle del pedido
    else:
        form = PedidoForm()
        productos = Producto.objects.all()

    return render(request, 'crear_pedido.html', {'form': form, 'productos': productos})


@login_required
@user_passes_test(is_superuser)
def registro_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_categoria')  # Asegúrate de tener una vista y URL para listar categorías
    else:
        form = CategoriaForm()
    return render(request, 'registro_categoria.html', {'form': form})