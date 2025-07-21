# 🎨 Sistema de Plantillas y Componentes Reutilizables de Vader

El Sistema de Plantillas de Vader permite crear aplicaciones complejas de manera rápida y sencilla usando plantillas predefinidas y componentes reutilizables.

## 🚀 **¿Qué son las Plantillas y Componentes?**

- **Plantillas**: Estructuras completas de aplicaciones que puedes personalizar con tus propios datos
- **Componentes**: Elementos reutilizables (botones, tarjetas, formularios) que puedes usar en cualquier proyecto

## 📦 **Plantillas Disponibles**

### 1. **Página Web Básica** (`web_basica`)
Crea una página web completa con navegación, contenido y formulario de contacto.

**Variables:**
- `titulo`: Título principal de la página
- `descripcion`: Descripción del sitio
- `autor`: Nombre del autor
- `color_principal`: Color principal del diseño

**Ejemplo de uso:**
```vader
usar plantilla "web_basica" con titulo="Mi Negocio", descripcion="La mejor empresa de la ciudad", autor="Juan Pérez", color_principal="azul"
```

### 2. **Aplicación React** (`app_react`)
Crea una aplicación React completa con navegación, estado y autenticación.

**Variables:**
- `nombre_app`: Nombre de la aplicación
- `titulo_principal`: Título que aparece en la navegación
- `descripcion_app`: Descripción de la aplicación

**Ejemplo de uso:**
```vader
usar plantilla "app_react" con nombre_app="MiApp", titulo_principal="Mi Aplicación Increíble", descripcion_app="Una app que cambiará tu vida"
```

## 🧩 **Componentes Disponibles**

### 1. **Botón Moderno** (`boton_moderno`)
Botón estilizado con efectos hover y diferentes variantes.

**Propiedades:**
- `texto`: Texto del botón
- `color`: Color del botón (azul, verde, rojo)
- `tamaño`: Tamaño del botón (pequeño, normal, grande)
- `accion`: Función JavaScript a ejecutar

**Ejemplo de uso:**
```vader
usar componente "boton_moderno" con texto="Enviar", color="azul", tamaño="grande", accion="enviarFormulario()"
```

### 2. **Tarjeta de Producto** (`tarjeta_producto`)
Tarjeta para mostrar productos con imagen, precio y botones de acción.

**Propiedades:**
- `nombre`: Nombre del producto
- `precio`: Precio del producto
- `imagen`: URL de la imagen
- `descripcion`: Descripción del producto
- `disponible`: "true" o "false" para disponibilidad

**Ejemplo de uso:**
```vader
usar componente "tarjeta_producto" con nombre="Laptop Gaming", precio="1299", imagen="laptop.jpg", descripcion="Laptop perfecta para gaming", disponible="true"
```

## 💡 **Cómo Usar el Sistema**

### Comandos Básicos

```vader
# Ver plantillas disponibles
listar plantillas

# Ver componentes disponibles
listar componentes

# Usar una plantilla
usar plantilla "nombre_plantilla" con variable1="valor1", variable2="valor2"

# Usar un componente
usar componente "nombre_componente" con prop1="valor1", prop2="valor2"
```

### Ejemplo Completo: Tienda Online

```vader
# Usar plantilla base para la estructura
usar plantilla "web_basica" con titulo="Mi Tienda Online", descripcion="Los mejores productos al mejor precio", autor="Mi Empresa", color_principal="verde"

# Agregar productos usando componentes
seccion id="productos"
    titulo2 "Nuestros Productos"
    
    div clase="productos-grid"
        usar componente "tarjeta_producto" con nombre="iPhone 15", precio="999", imagen="iphone15.jpg", descripcion="El último iPhone de Apple", disponible="true"
        
        usar componente "tarjeta_producto" con nombre="MacBook Pro", precio="2499", imagen="macbook.jpg", descripcion="Laptop profesional de Apple", disponible="true"
        
        usar componente "tarjeta_producto" con nombre="AirPods Pro", precio="249", imagen="airpods.jpg", descripcion="Auriculares inalámbricos premium", disponible="false"
    fin div
fin seccion

# Agregar botones de acción
div clase="acciones-principales"
    usar componente "boton_moderno" con texto="Ver Todos los Productos", color="azul", tamaño="grande", accion="verTodosProductos()"
    
    usar componente "boton_moderno" con texto="Contactar Ventas", color="verde", tamaño="normal", accion="contactarVentas()"
fin div
```

## 🎯 **Ventajas del Sistema de Plantillas**

### ✅ **Para Principiantes:**
- **Sin código complejo**: Solo necesitas cambiar variables y propiedades
- **Resultados profesionales**: Plantillas diseñadas por expertos
- **Aprendizaje gradual**: Puedes ver el código generado y aprender

### ✅ **Para Desarrolladores:**
- **Desarrollo rápido**: Crea aplicaciones en minutos, no horas
- **Consistencia**: Todos los componentes siguen las mismas convenciones
- **Personalizable**: Puedes modificar las plantillas según tus necesidades

### ✅ **Para Empresas:**
- **Prototipado rápido**: Crea demos y prototipos instantáneamente
- **Estándares uniformes**: Todos los proyectos siguen la misma estructura
- **Reducción de costos**: Menos tiempo de desarrollo

## 🛠️ **Crear Tus Propias Plantillas y Componentes**

### Crear una Plantilla

1. Crea un archivo JSON en la carpeta `plantillas/`
2. Define la estructura:

```json
{
  "name": "Mi Plantilla",
  "description": "Descripción de la plantilla",
  "variables": ["variable1", "variable2"],
  "framework": "html",
  "code": "código de la plantilla con {variable1} y {variable2}"
}
```

### Crear un Componente

1. Crea un archivo `.vdr` en la carpeta `componentes/`
2. Usa variables entre llaves: `{mi_variable}`
3. Incluye estilos y funcionalidad

## 🚀 **Comandos de Uso**

```bash
# Usar con plantilla
python3 src/vader.py mi_proyecto.vdr --target html --output index.html

# Ejemplo de archivo mi_proyecto.vdr:
# usar plantilla "web_basica" con titulo="Mi Sitio", autor="Yo"
# usar componente "boton_moderno" con texto="Empezar", color="azul"
```

## 🎨 **Próximas Plantillas y Componentes**

### Plantillas Planificadas:
- **Blog Personal**: Plantilla para blogs con artículos y comentarios
- **Dashboard Admin**: Panel de administración completo
- **Landing Page**: Página de aterrizaje para productos
- **E-commerce Completo**: Tienda online con carrito y checkout

### Componentes Planificados:
- **Formulario de Contacto**: Formulario completo con validación
- **Galería de Imágenes**: Galería responsive con lightbox
- **Navegación Móvil**: Menú hamburguesa responsive
- **Testimonios**: Carrusel de testimonios de clientes

## 💡 **¡Democratizando el Desarrollo!**

Con el Sistema de Plantillas de Vader, cualquier persona puede crear aplicaciones profesionales sin necesidad de conocimientos técnicos avanzados. Solo necesitas:

1. **Elegir una plantilla** que se adapte a tu necesidad
2. **Personalizar las variables** con tu información
3. **Agregar componentes** para funcionalidad extra
4. **¡Listo!** Tu aplicación está completa

¡El desarrollo de software nunca había sido tan accesible para todos!
