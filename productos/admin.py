from django.contrib import admin
from .models import Producto, Categoria, Etiqueta, DetalleProducto

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(DetalleProducto)
class DetalleProductoAdmin(admin.ModelAdmin):
    list_display = ('id','dimensiones','peso')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','precio','categoria','creado_en')
    list_filter = ('categoria','etiquetas')
    search_fields = ('nombre','descripcion')
    filter_horizontal = ('etiquetas',) # mejor UI para M2M