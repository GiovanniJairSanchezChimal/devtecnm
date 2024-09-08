from django.shortcuts import render, get_object_or_404, redirect
from registros.models import Pedido, Abono, Producto, Cliente, PedidoProducto, Talla, Categorias
from django.db.models import Sum, F
from datetime import datetime, timedelta
from registros.forms import PedidoForm, ProductoForm, ClienteForm, PedidoProductoForm, CategoriaForm
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test


def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    productos = pedido.pedido_productos.all()
    total_deuda = sum(pedido_producto.producto.precio_venta for pedido_producto in productos) - pedido.enganche
    total_abonos = sum(abono.cantidad for abono in pedido.abonos.all())
    deuda_restante = total_deuda - total_abonos

    context = {
        'pedido': pedido,
        'productos': productos,
        'total_deuda': total_deuda,
        'total_abonos': total_abonos,
        'deuda_restante': deuda_restante,
    }
    return render(request, 'detalle_pedido.html', context)

@login_required
@user_passes_test(is_superuser)
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    PedidoProductoFormSet = inlineformset_factory(Pedido, PedidoProducto, form=PedidoProductoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        formset = PedidoProductoFormSet(request.POST, instance=pedido)
        if form.is_valid() and formset.is_valid():
            # Guardar los cambios en el pedido
            form.save()

            # Guardar los cambios en los productos y tallas
            formset.save()

            return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        form = PedidoForm(instance=pedido)
        formset = PedidoProductoFormSet(instance=pedido)

    productos = Producto.objects.all()

    return render(request, 'editar_pedido.html', {'form': form, 'formset': formset, 'productos': productos})
@login_required
@user_passes_test(is_superuser)
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('lista_pedidos_semanal')
    return render(request, 'confirmar_eliminar_pedido.html', {'pedido': pedido})




@login_required
@user_passes_test(is_superuser)
def registrar_abono(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        cantidad = request.POST.get('cantidad')
        Abono.objects.create(pedido=pedido, cantidad=cantidad)
        return redirect('detalle_pedido', pedido_id=pedido.id)
    


@login_required
@user_passes_test(is_superuser)
def reporte_semanal(request):
    # Obtener la semana seleccionada desde el formulario
    semana = request.GET.get('semana')
    if semana:
        inicio_semana = datetime.strptime(semana + '-1', "%Y-W%W-%w")
        fin_semana = inicio_semana + timedelta(days=6)
    else:
        # Si no se selecciona una semana, usar la semana actual
        hoy = datetime.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

    pedidos = Pedido.objects.filter(fecha_realizacion__range=[inicio_semana, fin_semana])
    gasto_compra = pedidos.aggregate(total_gasto=Sum(F('productos__precio_compra')))['total_gasto']
    ganancia_recibida = pedidos.aggregate(total_ganancia=Sum(F('productos__ganancia')))['total_ganancia']
    venta_total = pedidos.aggregate(total_venta=Sum(F('productos__precio_venta')))['total_venta']

    context = {
        'pedidos': pedidos,
        'gasto_compra': gasto_compra,
        'ganancia_recibida': ganancia_recibida,
        'venta_total': venta_total,
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana,
    }
    return render(request, 'reporte_semanal.html', context)


@login_required
@user_passes_test(is_superuser)
def reporte_mensual(request):
    # Obtener el mes seleccionado desde el formulario
    mes = request.GET.get('mes')
    if mes:
        inicio_mes = datetime.strptime(mes, "%Y-%m")
        fin_mes = (inicio_mes + timedelta(days=31)).replace(day=1)
    else:
        # Si no se selecciona un mes, usar el mes actual
        hoy = datetime.today()
        inicio_mes = datetime(hoy.year, hoy.month, 1)
        fin_mes = (inicio_mes + timedelta(days=31)).replace(day=1)

    pedidos = Pedido.objects.filter(fecha_realizacion__range=[inicio_mes, fin_mes])
    gasto_compra = pedidos.aggregate(total_gasto=Sum(F('productos__precio_compra')))['total_gasto']
    ganancia_recibida = pedidos.aggregate(total_ganancia=Sum(F('productos__ganancia')))['total_ganancia']
    venta_total = pedidos.aggregate(total_venta=Sum(F('productos__precio_venta')))['total_venta']

    context = {
        'pedidos': pedidos,
        'gasto_compra': gasto_compra,
        'ganancia_recibida': ganancia_recibida,
        'venta_total': venta_total,
        'inicio_mes': inicio_mes,
        'fin_mes': fin_mes,
    }
    return render(request, 'reporte_mensual.html', context)



@login_required
@user_passes_test(is_superuser)
def lista_pedidos_semanal(request):
    # Obtener la semana seleccionada desde el formulario
    semana = request.GET.get('semana')
    if semana:
        inicio_semana = datetime.strptime(semana + '-1', "%Y-W%W-%w")
        fin_semana = inicio_semana + timedelta(days=6)
    else:
        # Si no se selecciona una semana, usar la semana actual
        hoy = datetime.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

    pedidos = Pedido.objects.filter(fecha_realizacion__range=[inicio_semana, fin_semana])
    pedidos_con_deuda = []

    for pedido in pedidos:
        total_deuda = sum(producto.precio_venta for producto in pedido.productos.all()) - pedido.enganche
        total_abonos = sum(abono.cantidad for abono in pedido.abonos.all())
        deuda_restante = total_deuda - total_abonos
        pedidos_con_deuda.append({
            'pedido': pedido,
            'deuda_restante': deuda_restante,
        })

    context = {
        'pedidos_con_deuda': pedidos_con_deuda,
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana,
    }
    return render(request, 'lista_pedidos_semanal.html', context)


@login_required
@user_passes_test(is_superuser)
def lista_productos(request):
    productos = Producto.objects.all()
    context = {
        'productos': productos,
    }
    return render(request, 'lista_productos.html', context)


@login_required
@user_passes_test(is_superuser)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'confirmar_eliminar_producto.html', {'producto': producto})

@login_required
@user_passes_test(is_superuser)
def lista_clientes(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes,
    }
    return render(request, 'lista_clientes.html', context)


@login_required
@user_passes_test(is_superuser)
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'confirmar_eliminar_cliente.html', {'cliente': cliente})


def lista_categorias(request):
    categorias = Categorias.objects.all()
    context = {
        'categorias': categorias,
    }
    return render(request, 'lista_categorias.html', context)


def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categorias, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categorias, id=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'confirmar_eliminar_categoria.html', {'categoria': categoria})