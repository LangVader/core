# 🚀 Guía Completa de Frameworks en Vader

Vader soporta más de 25 frameworks modernos, permitiendo crear cualquier tipo de aplicación escribiendo únicamente en español natural.

## 📱 **Frontend y Interfaces de Usuario**

### React - Biblioteca de Facebook
```vader
componente react "MiComponente"
    estado "contador" = 0
    
    efecto "componentDidMount"
        mostrar "Componente montado"
    fin efecto
    
    mostrar contador
    boton "Incrementar" onClick="incrementar"
fin componente
```

### Vue.js - Framework Progresivo
```vader
componente vue "Contador"
    reactivo "numero" = 0
    
    computed "doble"
        retornar numero * 2
    fin computed
    
    template
        mostrar "Contador: " + numero
        boton "+" @click="incrementar"
    fin template
fin componente
```

### Angular - Plataforma Empresarial
```vader
componente angular "AppComponent"
    propiedad "titulo" = "Mi App Angular"
    
    servicio "HttpClient"
    servicio "Router"
    
    metodo "ngOnInit"
        mostrar "Componente inicializado"
    fin metodo
fin componente
```

## 🌐 **Full-Stack y Meta-Frameworks**

### Next.js - React con SSR
```vader
pagina nextjs "/"
    servidor
        obtener datos
            retornar { props: { mensaje: "Hola desde servidor" } }
        fin obtener
    fin servidor
    
    cliente
        mostrar props.mensaje
    fin cliente
fin pagina
```

### Nuxt.js - Vue con SSR
```vader
pagina nuxt "/productos"
    async obtener datos
        productos = await $fetch('/api/productos')
        retornar { productos }
    fin obtener
    
    template
        repetir producto en productos
            mostrar producto.nombre
        fin repetir
    fin template
fin pagina
```

## ⚡ **Frameworks Modernos y Reactivos**

### SolidJS - Rendimiento Ultra Rápido
```vader
componente solid "Contador"
    señal "count" = 0
    
    efecto
        mostrar "Count cambió a: " + count()
    fin efecto
    
    mostrar count()
    boton "+" onClick={() => setCount(count() + 1)}
fin componente
```

### Svelte - Compilador Reactivo
```vader
componente svelte "TodoList"
    variable "todos" = []
    variable "nuevoTodo" = ""
    
    funcion "agregarTodo"
        todos = [...todos, nuevoTodo]
        nuevoTodo = ""
    fin funcion
    
    campo bind:value={nuevoTodo}
    boton on:click={agregarTodo} "Agregar"
fin componente
```

## 🔧 **Backend y APIs**

### Express.js - Node.js Minimalista
```vader
servidor express
    puerto 3000
    
    ruta get "/"
        responder "¡Hola desde Express!"
    fin ruta
    
    ruta post "/usuarios"
        usuario = req.body
        # Guardar usuario
        responder usuario
    fin ruta
    
    middleware "cors"
    middleware "json"
fin servidor
```

### FastAPI - Python Moderno
```vader
api fastapi
    ruta get "/usuarios"
        usuarios = obtener_todos_usuarios()
        retornar usuarios
    fin ruta
    
    ruta post "/usuarios"
        crear_usuario(usuario)
        retornar {"mensaje": "Usuario creado"}
    fin ruta
    
    modelo "Usuario"
        campo "nombre" str
        campo "email" str
        campo "edad" int
    fin modelo
fin api
```

### Spring Boot - Java Empresarial
```vader
controlador spring "ProductoController"
    inyectar "ProductoService"
    
    ruta get "/productos"
        productos = productoService.obtenerTodos()
        retornar ResponseEntity.ok(productos)
    fin ruta
    
    ruta post "/productos"
        producto = productoService.crear(nuevoProducto)
        retornar ResponseEntity.created(producto)
    fin ruta
fin controlador
```

## 🎨 **Desarrollo Web Moderno**

### Blazor - C# en el Navegador
```vader
componente blazor "Contador"
    estado "currentCount" = 0
    
    mostrar "Contador actual: " + currentCount
    
    boton "Incrementar" @onclick="IncrementCount"
    
    metodo "IncrementCount"
        currentCount++
    fin metodo
fin componente
```

### Flutter Web - Dart Multiplataforma
```vader
app flutter "MiApp"
    widget "HomePage"
        estado "contador" = 0
        
        scaffold
            appBar "Mi Aplicación Flutter"
            body
                columna
                    texto "Has presionado el botón:"
                    texto contador
                fin columna
            fin body
            
            floatingActionButton
                onPressed "incrementar"
                icono "add"
            fin floatingActionButton
        fin scaffold
    fin widget
fin app
```

## 📊 **Análisis de Datos y Ciencia**

### R Statistics - Análisis Estadístico
```vader
cargar datos "ventas.csv" como "ventas"

mostrar resumen ventas
histograma "precio"
grafico barras "categoria" por "ventas"

regresion lineal "ingresos" por "publicidad"
correlacion "precio, cantidad, descuento"

test t "satisfaccion" por "tipo_cliente"
anova "ventas" por "region"

guardar grafico "analisis_ventas.png"
exportar datos "resultados.csv"
```

### Scala - Big Data y Programación Funcional
```vader
objeto scala "AnalisisDatos"
    lista inmutable "numeros" = [1, 2, 3, 4, 5]
    
    filtrar numeros donde "x > 2"
    mapear numeros con "x * 2"
    reducir numeros con "_ + _"
    
    spark "procesamiento distribuido"
        cargar "datos.parquet"
        filtrar "edad > 18"
        agrupar por "ciudad"
        guardar "resultado.parquet"
    fin spark
fin objeto
```

## 🔥 **Frameworks Especializados**

### Astro - Sitios Estáticos Modernos
```vader
pagina astro "blog"
    frontmatter
        titulo = "Mi Blog"
        fecha = "2024-01-01"
    fin frontmatter
    
    componente "Header" titulo={titulo}
    
    contenido
        titulo1 titulo
        parrafo "Bienvenido a mi blog personal"
    fin contenido
    
    script cliente
        mostrar "Página cargada"
    fin script
fin pagina
```

### Qwik - Resumabilidad Extrema
```vader
componente qwik "App"
    señal "count" = 0
    
    tarea visible
        mostrar "Componente visible"
    fin tarea
    
    mostrar "Contador: " + count.value
    boton onClick$={() => count.value++} "+"
fin componente
```

## 💡 **Cómo Elegir el Framework Correcto**

### Para Sitios Web Simples:
- **HTML/CSS Natural** - Páginas estáticas
- **Astro** - Sitios con algo de interactividad

### Para Aplicaciones Web:
- **React** - Ecosistema maduro, muchos recursos
- **Vue** - Curva de aprendizaje suave
- **Angular** - Aplicaciones empresariales grandes

### Para Rendimiento Extremo:
- **SolidJS** - Máximo rendimiento
- **Svelte** - Compilación optimizada
- **Qwik** - Carga instantánea

### Para Full-Stack:
- **Next.js** - React con SSR
- **Nuxt.js** - Vue con SSR
- **SvelteKit** - Svelte full-stack

### Para Backend:
- **Express** - Node.js simple
- **FastAPI** - Python moderno
- **Spring Boot** - Java empresarial

### Para Análisis:
- **R Statistics** - Análisis estadístico
- **Scala** - Big data y Spark

## 🚀 **Comandos Útiles**

```bash
# Ver todos los frameworks disponibles
python3 src/vader.py --list-frameworks

# Usar framework específico
python3 src/vader.py mi_app.vdr --framework react --target javascript
python3 src/vader.py mi_api.vdr --framework fastapi --target python
python3 src/vader.py analisis.vdr --framework r_stats --target r

# Detección automática
python3 src/vader.py mi_codigo.vdr --target javascript --verbose
```

## 🎯 **Próximos Frameworks**

- **Gin/Echo** (Go) - APIs ultra rápidas
- **Actix/Axum** (Rust) - Rendimiento extremo
- **Phoenix** (Elixir) - Tiempo real
- **Rails** (Ruby) - Desarrollo rápido

¡Con Vader puedes crear cualquier aplicación moderna escribiendo únicamente en español natural!
