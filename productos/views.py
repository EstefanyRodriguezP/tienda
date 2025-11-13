from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q, F, Count, Avg, Max
from .models import Producto, Categoria, Etiqueta, DetalleProducto
from .forms import ProductoForm, CategoriaForm, EtiquetaForm, DetalleProductoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    # Estadísticas
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_etiquetas = Etiqueta.objects.count()

    # Promedio y máximo precio
    promedio_precio = Producto.objects.aggregate(avg=Avg('precio'))['avg'] or 0
    max_precio = Producto.objects.aggregate(max=Max('precio'))['max']

    # Producto más caro (si existe)
    producto_mas_caro = None
    if max_precio is not None:
        producto_mas_caro = Producto.objects.filter(precio=max_precio).first()

    # Últimos productos (ordenados por creado_en)
    ultimos_productos = Producto.objects.select_related('categoria').prefetch_related('etiquetas').order_by('-creado_en')[:6]

    # Categorías con contador
    categorias = Categoria.objects.annotate(num_productos=Count('productos')).order_by('-num_productos')[:6]

    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_etiquetas': total_etiquetas,
        'promedio_precio': promedio_precio,
        'producto_mas_caro': producto_mas_caro,
        'ultimos_productos': ultimos_productos,
        'categorias': categorias,
    }
    return render(request, 'productos/index.html', context)

# Productos
def lista_productos(request):
    # Recuperar todos los productos con relaciones para optimizar consultas
    qs = Producto.objects.select_related('categoria','detalle').prefetch_related('etiquetas').all()

    # filtros simples desde query params
    q = request.GET.get('q')
    cat = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')

    if q:
        qs = qs.filter(nombre__icontains=q)
    if cat:
        qs = qs.filter(categoria_id=cat)
    if precio_min:
        try:
            qs = qs.filter(precio__gte=float(precio_min))
        except ValueError:
            pass

    context = {
        'titulo': 'Lista de Productos',
        'items': qs,
        'tipo': 'productos',
        'categorias': Categoria.objects.all(), # para dropdown de filtros
    }
    return render(request, 'productos/lista.html', context)

def detalle_producto(request, id):
    producto = get_object_or_404(Producto.objects.select_related('categoria','detalle').prefetch_related('etiquetas'), pk=id)
    context = {'producto': producto}
    return render(request, 'productos/detalle.html', context)

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        detalle_form = DetalleProductoForm(request.POST)
        if form.is_valid() and detalle_form.is_valid():
            detalle = detalle_form.save()
            producto = form.save(commit=False)
            producto.detalle = detalle
            producto.save()
            form.save_m2m()
            messages.success(request, "Producto creado correctamente.")
            return redirect('lista_productos')
    else:
        form = ProductoForm()
        detalle_form = DetalleProductoForm()
    return render(request, 'productos/crear.html', {'form': form, 'detalle_form': detalle_form})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    detalle = producto.detalle or DetalleProducto()
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        detalle_form = DetalleProductoForm(request.POST, instance=detalle)
        if form.is_valid() and detalle_form.is_valid():
            detalle = detalle_form.save()
            producto = form.save(commit=False)
            producto.detalle = detalle
            producto.save()
            form.save_m2m()
            messages.success(request, "Producto actualizado.")
            return redirect('detalle_producto', id=producto.id)
    else:
        form = ProductoForm(instance=producto)
        detalle_form = DetalleProductoForm(instance=detalle)
    return render(request, 'productos/editar.html', {'form': form, 'detalle_form': detalle_form, 'producto': producto})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado.")
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {
        'tipo': 'producto',
        'nombre_objeto': producto.nombre,
        'lista_url': reverse('lista_productos')
    })

# Categorías
def lista_categorias(request):
    categorias = Categoria.objects.annotate(num_productos=Count('productos'))
    return render(request, 'productos/lista.html', {
        'titulo': 'Lista de Categorías',
        'items': categorias,
        'tipo': 'categorias',
    })

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'productos/form.html', {'form': form, 'tipo': 'categoria'})

def editar_categoria(request, id):
    cat = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=cat)
    return render(request, 'productos/form.html', {'form': form, 'tipo': 'categoria'})

def eliminar_categoria(request, id):
    cat = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':
        cat.delete()
        return redirect('lista_categorias')
    return render(request, 'productos/eliminar.html', {
        'tipo': 'categoría',
        'nombre_objeto': cat.nombre,
        'lista_url': reverse('lista_categorias')
    })

# Etiquetas
def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'productos/lista.html', {
        'titulo': 'Lista de Etiquetas',
        'items': etiquetas,
        'tipo': 'etiquetas',
    })

def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm()
    return render(request, 'productos/form.html', {'form': form, 'tipo': 'etiqueta'})

def editar_etiqueta(request, id):
    et = get_object_or_404(Etiqueta, pk=id)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=et)
        if form.is_valid():
            form.save()
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm(instance=et)
    return render(request, 'productos/form.html', {'form': form, 'tipo': 'etiqueta'})

def eliminar_etiqueta(request, id):
    et = get_object_or_404(Etiqueta, pk=id)
    if request.method == 'POST':
        et.delete()
        return redirect('lista_etiquetas')
    return render(request, 'productos/eliminar.html', {
        'tipo': 'etiqueta',
        'nombre_objeto': et.nombre,
        'lista_url': reverse('lista_etiquetas')
    })