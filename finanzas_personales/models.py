from django.db import models


class Ingreso(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fuente = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.fuente} - {self.monto}"

class Gasto(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('CategoriaGasto', on_delete=models.CASCADE, related_name='gastos')
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.monto}"

class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Ahorro(models.Model):
    monto_objetivo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descripcion = models.CharField(max_length=200)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.descripcion} - {self.monto_actual}/{self.monto_objetivo}"


class Inversion(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - {self.monto}"

class Presupuesto(models.Model):
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE, related_name='presupuestos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Presupuesto para {self.categoria.nombre} - {self.monto}"

class Deuda(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Pagada', 'Pagada')])

    def __str__(self):
        return f"{self.descripcion} - {self.monto} ({self.estado})"


class Transaccion(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=[('Ingreso', 'Ingreso'), ('Gasto', 'Gasto')])
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.CASCADE, related_name='transacciones')
    descripcion = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - {self.monto}"
