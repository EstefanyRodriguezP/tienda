from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class DetalleProducto(models.Model):
    # Relación OneToOne con Producto — definida abajo con 'Producto' referencia
    dimensiones = models.CharField(max_length=100, blank=True) # ej "10x20x5 cm"
    peso = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) # kg por ejemplo

    def __str__(self):
        return f"Detalle ({self.id})"

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='productos')
    # OneToOne hacia DetalleProducto — usa related_name para acceder desde producto
    detalle = models.OneToOneField(DetalleProducto, on_delete=models.CASCADE, null=True, blank=True, related_name='producto')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre