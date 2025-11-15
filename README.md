# 🛍️ Tienda - Gestión de Productos con Django y MySQL

Aplicación web desarrollada con **Django** que permite gestionar una lista de productos, sus categorías, etiquetas y detalles.  
Incluye operaciones **CRUD completas**, conexión a **MySQL**, y el uso del **ORM de Django** para realizar consultas avanzadas.

---

## 🚀 Características principales

- Conexión a base de datos **MySQL**
- Modelos relacionados:
  - **Producto** ↔ **Categoría** → Relación Muchos a Uno
  - **Producto** ↔ **Etiqueta** → Relación Muchos a Muchos
  - **Producto** ↔ **DetalleProducto** → Relación Uno a Uno
- Interfaz CRUD completa:
  - Crear, listar, editar y eliminar productos, categorías y etiquetas
- Consultas ORM con filtros, exclusiones y consultas personalizadas
- Uso del **Django Admin**
- Protección CSRF y middleware de seguridad activado

---

## 🗂️ Estructura del proyecto
```bash
tienda
 ┣ productos
 ┃ ┣ migrations
 ┃ ┣ templates
 ┃ ┣ admin.py
 ┃ ┣ apps.py
 ┃ ┣ forms.py
 ┃ ┣ models.py
 ┃ ┣ tests.py
 ┃ ┣ urls.py
 ┃ ┣ views.py
 ┃ ┗ __init__.py
 ┣ screenshots
 ┣ tienda
 ┃ ┣ asgi.py
 ┃ ┣ settings.py
 ┃ ┣ urls.py
 ┃ ┣ wsgi.py
 ┃ ┗ __init__.py
 ┣ manage.py
 ┣ README.md
 ┗ requirements.txt
```

---
## ⚙️ Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/EstefanyRodriguezP/tienda.git
cd tienda
```
### 2. Crear y activar entorno virtual
```bash
python -m venv django_env
source django_env/Scripts/activate   # En Windows
# o
source django_env/bin/activate       # En macOS/Linux
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Configurar la base de datos MySQL
Asegúrate de tener MySQL en ejecución y crea la base de datos:
```bash
CREATE DATABASE IF NOT EXISTS tienda_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tienda_db;
```
Edita tienda/settings.py con tus credenciales:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tienda_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
### 5. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Crear superusuario
```bash
python manage.py createsuperuser
```
### 7. Ejecutar servidor
```bash
python manage.py runserver
```
Luego abre tu navegador en:
👉 http://127.0.0.1:8000/

---
## 💾 Integración de Django con bases de datos

Django permite conectarse a distintos motores de bases de datos, como SQLite (por defecto), MySQL, PostgreSQL y Oracle. La conexión se gestiona desde el archivo `settings.py` mediante la configuración del diccionario `DATABASES`.  

El ORM (Object-Relational Mapper) de Django permite trabajar con la base de datos utilizando objetos Python, evitando escribir sentencias SQL manuales en la mayoría de los casos. Las operaciones CRUD (crear, leer, actualizar, eliminar) se realizan a través de métodos como `.create()`, `.get()`, `.filter()`, `.update()` y `.delete()`.  

**Ejemplo:**  
En `settings.py` se define la conexión con MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tienda_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Django maneja automáticamente las conexiones y el cierre de estas cuando se ejecutan consultas a través del ORM.
---
## 🧩 Modelos implementados

### 🛒 Producto
- nombre: CharField
- descripcion: TextField
- precio: DecimalField
- categoria: ForeignKey → Categoria
- etiquetas: ManyToManyField → Etiqueta
- detalle: OneToOneField → DetalleProducto

### 🏷️ Categoría
- nombre: CharField
- Relación: una categoría puede tener muchos productos.

### 🔖 Etiqueta
- nombre: CharField
- Relación: un producto puede tener muchas etiquetas y viceversa.

### ⚙️ DetalleProducto
- nombre: CharField
- dimensiones: CharField
- Relación: uno a uno con Producto.


### 📦 Modelo sin relaciones

Se puede implementar un modelo simple sin relaciones, que genere una tabla independiente en la base de datos.

**Ejemplo:**

```python
from django.db import models

class ProductoSimple(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
```
Este modelo no se relaciona con ninguna otra tabla y puede ser gestionado con migraciones y el ORM de Django.

### 🔗 Modelos con relaciones

- **OneToOneField**: `Producto` ↔ `DetalleProducto` (un producto tiene un detalle único)  
- **ForeignKey**: `Producto` ↔ `Categoria` (una categoría puede tener muchos productos)  
- **ManyToManyField**: `Producto` ↔ `Etiqueta` (un producto puede tener muchas etiquetas y viceversa)  

**Ejemplo de uso:**
```python
# Crear un detalle de producto
detalle = DetalleProducto.objects.create(dimensiones="10x20x5", peso="1kg")
# Asociar detalle a producto
producto = Producto.objects.create(nombre="Laptop", precio=1000, categoria=categoria)
producto.detalle = detalle
producto.etiquetas.set([etiqueta1, etiqueta2])
```

### 🔄 Migraciones

Para propagar los cambios de los modelos a la base de datos, Django utiliza migraciones.  

**Ejemplo:**

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate
```
Si se agrega un nuevo campo o modelo, estas instrucciones actualizan automáticamente el esquema en MySQL.


### 🖥️ Aplicación CRUD

Esta aplicación implementa el patrón MVC mediante:

- **Modelos**: `Producto`, `Categoria`, `Etiqueta`, `DetalleProducto`  
- **Vistas**: funciones en `views.py` para crear, listar, editar y eliminar registros  
- **Templates**: HTML con Bootstrap para mostrar formularios y listas  
- **URLs**: rutas en `urls.py` que llaman a las vistas correspondientes  

**Ejemplo:** eliminar un producto:

```python
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, pk=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, "Producto eliminado.")
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})
```

---

## 🧭 Rutas principales (URLConf)


| Ruta                        | Descripción         |
| --------------------------- | ------------------- |
| `/`                         | Página de inicio    |
| `/productos/`               | Lista de productos  |
| `/productos/crear/`         | Crear producto      |
| `/productos/<id>/`          | Detalle de producto |
| `/productos/<id>/editar/`   | Editar producto     |
| `/productos/<id>/eliminar/` | Eliminar producto   |
| `/categorias/`              | Lista de categorías |
| `/categorias/crear/`        | Crear categoría     |
| `/etiquetas/`               | Lista de etiquetas  |
| `/etiquetas/crear/`         | Crear etiqueta      |

---

## 🧠 Creación datos de ejemplo mediante ORM

### Creación de categorías
![Creación categorías](screenshots/categorias_ORM.png)
---
### Creación de etiquetas
![Creación etiquetas](screenshots/etiquetas_ORM.png)
---
### Creación de productos
![Creación productos](screenshots/productos_ORM.png)
---
### Asociar etiquetas a los productos
![Asociar etiquetas a los productos](screenshots/etiquetas_productos.png)
---
### Consultas de prueba
![Consultas de prueba](screenshots/consultas.png)


---

## 🧠 Otras consultas con ORM y SQL de ejemplo

Django ORM permite consultas de filtrado, exclusión, ordenamiento y anotaciones:

```python
# Filtrar productos por categoría
Producto.objects.filter(categoria__nombre="Electrónica")

# Excluir productos de una categoría
Producto.objects.exclude(categoria__nombre="Hogar")

# Productos con precio mayor a 50000
Producto.objects.filter(precio__gt=50000)

# Consultas con etiquetas
Producto.objects.filter(etiquetas__nombre="Oferta")

# Ordenar productos por precio descendente
Producto.objects.all().order_by('-precio')
```

Para consultas más avanzadas, se puede usar raw() para ejecutar SQL directamente:

```python
Producto.objects.raw("SELECT * FROM productos_producto WHERE precio > 50000")
```
```sql
SELECT * FROM productos_producto WHERE precio > 50000;
```

---

## 🖼️ Capturas de pantalla

### Página de inicio
![Inicio](screenshots/inicio.png)
---
### Lista de productos
![Productos](screenshots/productos.png)
---
### Detalle producto
![Detalle producto](screenshots/detalle_producto.png)
---
### Crear producto
![Crear producto](screenshots/crear_producto.png)
---
### Eliminar etiqueta
![Eliminar etiqueta](screenshots/eliminar_etiqueta.png)
---
### Panel de administración
![Admin](screenshots/admin.png)


---
## ⚙️ Aplicaciones preinstaladas

Django incluye aplicaciones listas para usar que facilitan el desarrollo:

- **django.contrib.admin** → Panel de administración
- **django.contrib.auth** → Gestión de usuarios y permisos
- **django.contrib.sessions** → Manejo de sesiones
- **django.contrib.messages** → Mensajes flash en la UI
- **django.contrib.staticfiles** → Gestión de archivos estáticos  

**Ejemplo:** `admin.py` registra los modelos para el panel de administración:

```python
from django.contrib import admin
from .models import Producto, Categoria, Etiqueta, DetalleProducto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','precio','categoria','creado_en')
    list_filter = ('categoria','etiquetas')
```

---

## 📚 Autor
👩‍💻 Estefany Rodríguez Pérez
Repositorio GitHub: EstefanyRodriguezP

---

## 🧾 Licencia
Este proyecto se entrega con fines educativos, como parte del proceso de evaluación del módulo Django del Bootcamp Full Stack Python.