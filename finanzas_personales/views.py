from django.shortcuts import render, redirect
from .models import Ingreso, Gasto, CategoriaGasto, Ahorro, Inversion, Presupuesto, Deuda, Transaccion
from .forms import IngresoForm, GastoForm, CategoriaGastoForm, AhorroForm, InversionForm, PresupuestoForm, DeudaForm, TransaccionForm
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ingreso, Gasto, Ahorro, Inversion, Presupuesto, Deuda, Transaccion
from . import models
import io
from django.http import HttpResponseBadRequest

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def registrar_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_ingreso')
    else:
        form = IngresoForm()
    return render(request, 'registrar_ingreso.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def registrar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_gasto')
    else:
        form = GastoForm()
    return render(request, 'registrar_gasto.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def registrar_categoria_gasto(request):
    if request.method == 'POST':
        form = CategoriaGastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_categoria_gasto')
    else:
        form = CategoriaGastoForm()
    return render(request, 'registrar_categoria_gasto.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def registrar_ahorro(request):
    if request.method == 'POST':
        form = AhorroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_ahorro')
    else:
        form = AhorroForm()
    return render(request, 'registrar_ahorro.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def registrar_inversion(request):
    if request.method == 'POST':
        form = InversionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_inversion')
    else:
        form = InversionForm()
    return render(request, 'registrar_inversion.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def registrar_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_presupuesto')
    else:
        form = PresupuestoForm()
    return render(request, 'registrar_presupuesto.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def registrar_deuda(request):
    if request.method == 'POST':
        form = DeudaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_deuda')
    else:
        form = DeudaForm()
    return render(request, 'registrar_deuda.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def registrar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_transaccion')
    else:
        form = TransaccionForm()
    return render(request, 'registrar_transaccion.html', {'form': form})




@login_required
@user_passes_test(is_superuser)
def reporte_mensual_finanzas(request):
    mes = request.GET.get('mes', '')

    if not mes:
        # Obtener el mes actual en formato YYYY-MM
        today = datetime.today()
        mes = today.strftime('%Y-%m')

    try:
        # Asegúrate de que el formato del mes es correcto
        year, month = mes.split('-')
        year = int(year)
        month = int(month)
        
        # Filtrar los datos por mes
        ingresos = Ingreso.objects.filter(fecha__year=year, fecha__month=month)
        deudas = Deuda.objects.filter(fecha__year=year, fecha__month=month)
        gastos = Gasto.objects.filter(fecha__year=year, fecha__month=month)
        ahorros = Ahorro.objects.filter(fecha_inicio__year=year, fecha_inicio__month=month)
        inversiones = Inversion.objects.filter(fecha__year=year, fecha__month=month)
        transacciones = Transaccion.objects.filter(fecha__year=year, fecha__month=month)

        # Cálculo de totales
        total_ingresos = ingresos.aggregate(total=Sum('monto'))['total'] or 0
        total_deudas = deudas.aggregate(total=Sum('monto'))['total'] or 0
        total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0
        total_inversiones = inversiones.aggregate(total=Sum('monto'))['total'] or 0

        # Cálculo de utilidad neta
        utilidad_neta = total_ingresos - total_deudas

        contexto = {
            'inicio_mes': mes,
            'current_month': datetime.today().strftime('%Y-%m'),
            'total_ingresos': total_ingresos,
            'total_deudas': total_deudas,
            'total_gastos': total_gastos,
            'total_inversiones': total_inversiones,
            'utilidad_neta': utilidad_neta,
            'ingresos': ingresos,
            'deudas': deudas,
            'gastos': gastos,
            'ahorros': ahorros,
            'inversiones': inversiones,
            'transacciones': transacciones,
        }

        return render(request, 'reporte_mensual_finanzas.html', contexto)
    except ValueError:
        return HttpResponseBadRequest("El parámetro del mes tiene un formato incorrecto.")