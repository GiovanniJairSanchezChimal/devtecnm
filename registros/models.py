from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre}"
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, null=True, related_name='productos')
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    ganancia = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    def calcular_ganancia(self):
        self.ganancia = self.precio_venta - self.precio_compra
        return self.ganancia

    def save(self, *args, **kwargs):
        self.calcular_ganancia()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Talla(models.Model):
    talla = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f"Talla: {self.talla}"
    
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=False, related_name='cliente')
    productos = models.ManyToManyField(Producto, through='PedidoProducto', related_name='pedidos')
    enganche = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_realizacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.cliente} realizado el {self.fecha_realizacion}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pedido_productos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto.nombre} - Talla: {self.talla.talla}"


    
class Abono(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='abonos')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Abono de {self.cantidad} para el pedido {self.pedido.id}"
