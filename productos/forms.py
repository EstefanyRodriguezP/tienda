from django import forms
from .models import Producto, Categoria, Etiqueta, DetalleProducto

class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ['dimensiones','peso']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','categoria','etiquetas']
        widgets = {
            'etiquetas': forms.CheckboxSelectMultiple(),
            'descripcion': forms.Textarea(attrs={'rows':3}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion']

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre']