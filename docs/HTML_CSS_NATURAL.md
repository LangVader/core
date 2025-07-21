# HTML y CSS Natural con Vader

Vader ahora incluye soporte completo para crear páginas web usando sintaxis natural en español. Puedes crear HTML y CSS sin aprender estos lenguajes técnicos.

## ¿Qué es HTML y CSS Natural?

- **HTML Natural**: Crea la estructura de tu página web escribiendo en español
- **CSS Natural**: Define los estilos y diseño de tu página usando palabras cotidianas
- **Sin código técnico**: No necesitas aprender etiquetas HTML ni propiedades CSS

## Sintaxis HTML Natural

### Estructura Básica de una Página

```vader
pagina "Título de mi página"
    encabezado
        titulo1 "Mi sitio web"
        parrafo "Descripción de mi sitio"
    fin encabezado
    
    contenido
        seccion "principal"
            titulo2 "Bienvenido"
            parrafo "Este es el contenido principal"
        fin seccion
    fin contenido
    
    pie_pagina
        parrafo "© 2024 Mi Sitio Web"
    fin pie_pagina
fin pagina
```

### Elementos HTML Disponibles

#### Títulos
```vader
titulo1 "Título principal"          # <h1>
titulo2 "Título secundario"         # <h2>
titulo3 "Subtítulo"                 # <h3>
```

#### Texto
```vader
parrafo "Este es un párrafo"        # <p>
```

#### Enlaces
```vader
enlace "texto del enlace" "https://ejemplo.com"    # <a>
```

#### Botones
```vader
boton "Hacer clic aquí"             # <button>
```

#### Imágenes
```vader
imagen "foto.jpg" "Descripción de la imagen"       # <img>
```

#### Listas
```vader
lista "mi_lista"
    elemento "Primer elemento"
    elemento "Segundo elemento"
    elemento "Tercer elemento"
fin lista
```

#### Formularios
```vader
formulario "contacto"
    campo "nombre" "text" "Tu nombre"
    campo "email" "email" "Tu email"
    campo "mensaje" "textarea" "Tu mensaje"
    boton "Enviar"
fin formulario
```

#### Estructura y Secciones
```vader
encabezado          # <header>
navegacion          # <nav>
contenido           # <main>
seccion "nombre"    # <section>
tarjeta "nombre"    # <div class="card">
pie_pagina          # <footer>
```

## Sintaxis CSS Natural

### Estructura Básica de Estilos

```vader
estilos
    cuerpo
        fuente = "arial"
        tamaño_fuente = "16px"
        color = "negro"
        fondo_color = "blanco"
    fin cuerpo
    
    titulo1
        tamaño_fuente = "2rem"
        color = "azul"
        peso_fuente = "negrita"
    fin titulo1
fin estilos
```

### Propiedades CSS Disponibles

#### Colores
```vader
color = "rojo"              # Colores en español
fondo_color = "azul"        # background-color
fondo_gradiente = "azul a verde"  # gradientes
```

**Colores disponibles**: rojo, azul, verde, amarillo, morado, naranja, rosa, gris, negro, blanco, transparente

#### Fuentes y Texto
```vader
fuente = "arial"            # font-family
tamaño_fuente = "18px"      # font-size
peso_fuente = "negrita"     # font-weight
estilo_fuente = "cursiva"   # font-style
alineacion_texto = "centro" # text-align
decoracion_texto = "subrayado"  # text-decoration
```

#### Espaciado
```vader
margen = "10px"             # margin
margen_arriba = "20px"      # margin-top
relleno = "15px"            # padding
relleno_izquierda = "10px"  # padding-left
```

#### Tamaños
```vader
ancho = "100%"              # width
alto = "200px"              # height
ancho_maximo = "800px"      # max-width
```

#### Bordes y Sombras
```vader
borde = "2px solid negro"   # border
borde_radio = "10px"        # border-radius
sombra = "0 2px 10px rgba(0,0,0,0.1)"  # box-shadow
```

#### Posicionamiento
```vader
posicion = "relativa"       # position
mostrar = "flex"            # display
flotante = "izquierda"      # float
```

### Estados Interactivos

#### Hover (al pasar el mouse)
```vader
boton
    fondo_color = "azul"
    
    al_pasar_mouse
        fondo_color = "azul oscuro"
        transformar = "scale(1.05)"
    fin hover
fin boton
```

#### Active (al hacer clic)
```vader
boton
    al_hacer_click
        transformar = "scale(0.98)"
    fin active
fin boton
```

### Diseño Responsive

```vader
responsive
    en_movil
        cuerpo
            tamaño_fuente = "14px"
        fin cuerpo
    fin movil
    
    en_tablet
        contenido
            ancho_maximo = "768px"
        fin contenido
    fin tablet
    
    en_escritorio
        contenido
            ancho_maximo = "1200px"
        fin contenido
    fin escritorio
fin responsive
```

### Animaciones

```vader
animacion "fadeIn"
    desde
        opacidad = "0"
        transformar = "translateY(30px)"
    fin desde
    
    hasta
        opacidad = "1"
        transformar = "translateY(0)"
    fin hasta
fin animacion
```

## Cómo Usar HTML y CSS Natural

### 1. Crear un archivo HTML
```bash
# Crear archivo .vdr con contenido HTML
python3 src/vader.py mi_pagina.vdr --target html --output mi_pagina.html
```

### 2. Crear un archivo CSS
```bash
# Crear archivo .vdr con estilos CSS
python3 src/vader.py mis_estilos.vdr --target css --output mis_estilos.css
```

### 3. Detección Automática
Vader detecta automáticamente si tu código contiene HTML o CSS y usa el transpilador correcto.

## Ejemplos Completos

### Ejemplo 1: Página Personal Simple
Ver: `ejemplos/html_css/ejemplo_simple.vdr`

### Ejemplo 2: Página Personal Completa
Ver: `ejemplos/html_css/pagina_personal.vdr`

### Ejemplo 3: Tienda Online
Ver: `ejemplos/html_css/tienda_online.vdr`

### Ejemplo 4: Estilos Modernos
Ver: `ejemplos/html_css/estilos_modernos.vdr`

## Ventajas del HTML/CSS Natural

1. **Accesible**: Cualquier persona puede crear páginas web sin conocimientos técnicos
2. **Intuitivo**: Usa palabras en español que todos entienden
3. **Completo**: Genera HTML5 semántico y CSS3 moderno
4. **Responsive**: Soporte nativo para diseño adaptable
5. **Moderno**: Incluye animaciones, gradientes y efectos avanzados

## Consejos y Mejores Prácticas

1. **Estructura clara**: Usa encabezado, contenido y pie_pagina para organizar tu página
2. **Secciones**: Divide tu contenido en secciones lógicas
3. **Clases**: Usa nombres descriptivos para tus secciones y tarjetas
4. **Responsive**: Siempre incluye estilos responsive para móviles
5. **Colores**: Usa la paleta de colores en español para consistencia

## Próximas Características

- Más elementos HTML (tablas, videos, audio)
- Más propiedades CSS (grid, flexbox avanzado)
- Componentes reutilizables
- Temas predefinidos
- Integración con frameworks web

¡Con Vader, crear páginas web es tan fácil como escribir en español!
