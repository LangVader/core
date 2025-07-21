# 🗣️ Programar en Vader es Como Hablar con un Amigo

> **"Si puedes decirlo, puedes programarlo"**

---

## 🌟 ¡La Revolución de la Programación Natural!

**Vader ahora es tan fácil que programar es literalmente como hablar.** No hay palabras técnicas, no hay símbolos raros, no hay nada confuso. Solo escribes lo que quieres que haga tu computadora, ¡exactamente como se lo dirías a un amigo!

---

## 💬 Habla con tu Computadora

### 🗨️ **Para que diga algo:**
```vader
decir "Hola, soy tu computadora"
decir "¿Cómo estás hoy?"
```
*Es como decirle a alguien: "Di hola"*

### 👂 **Para que te escuche:**
```vader
preguntar "¿Cómo te llamas?"
guardar la respuesta en mi_nombre
```
*Es como decir: "Pregúntale su nombre y recuerda lo que diga"*

### 🧮 **Para hacer cuentas:**
```vader
preguntar "¿Cuánto es 5 + 3?"
guardar la respuesta en numero
convertir numero a número
resultado = numero * 2
decir "El doble es: " + resultado
```
*Es como pedirle a alguien que haga matemáticas*

---

## 🤔 Tomar Decisiones (Como Humanos)

### ✅ **Si algo es verdad, haz esto:**
```vader
preguntar "¿Cuántos años tienes?"
guardar la respuesta en edad
convertir edad a número

si edad es mayor que 18
    decir "Eres adulto"
si no
    decir "Eres joven"
terminar
```

### 🔄 **Repetir cosas (como cuando insistes):**
```vader
# Repetir algo varias veces
repetir 3 veces
    decir "¡Te quiero!"
terminar

# Repetir con una lista (como saludar a todos tus amigos)
mis_amigos = ["Ana", "Luis", "María"]
repetir con cada amigo en mis_amigos
    decir "Hola " + amigo
terminar
```

---

## 👥 Crear "Tipos de Cosas" (Como Describir Personas)

### 🧑 **Describir cómo es una persona:**
```vader
tipo de cosa llamada Persona
    guardar nombre
    guardar edad
    guardar hobby_favorito
    
    hacer presentacion
        decir "Hola, soy " + self.nombre
        decir "Tengo " + self.edad + " años"
        decir "Me gusta " + self.hobby_favorito
    terminar
    
    hacer cumplir_anos
        self.edad = self.edad + 1
        decir "¡Ahora tengo " + self.edad + " años!"
    terminar
terminar
```

### 🏗️ **Crear personas nuevas:**
```vader
# Crear una persona
ana = Persona()
ana.nombre = "Ana"
ana.edad = 25
ana.hobby_favorito = "leer"

# Hacer que se presente
llamar ana.presentacion()

# Hacer que cumpla años
llamar ana.cumplir_anos()
```

---

## 🛠️ Crear "Acciones" (Como Enseñar Trucos)

### 🎯 **Enseñarle a hacer algo específico:**
```vader
hacer saludar_bonito con nombre y edad
    decir "¡Hola " + nombre + "!"
    decir "Qué genial que tengas " + edad + " años"
    decir "¡Espero que tengas un día increíble!"
    devolver "Saludo completado"
terminar

# Usar la acción que le enseñamos
resultado = saludar_bonito("Pedro", "30")
decir resultado
```

### 🧮 **Enseñarle matemáticas:**
```vader
hacer calcular_propina con cuenta y porcentaje
    propina = cuenta * porcentaje / 100
    total = cuenta + propina
    
    decir "Cuenta: $" + cuenta
    decir "Propina (" + porcentaje + "%): $" + propina
    decir "Total a pagar: $" + total
    
    devolver total
terminar

# Calcular la propina de una cena
total_a_pagar = calcular_propina(50, 15)
```

---

## 🎮 Ejemplos Súper Divertidos

### 🎯 **Juego de Adivinanzas:**
```vader
decir "🎯 ¡Vamos a jugar!"
decir "Piensa en un número del 1 al 10"

mi_numero_secreto = 7
intentos = 0

repetir siempre
    preguntar "¿Cuál es tu número?"
    guardar la respuesta en tu_numero
    convertir tu_numero a número
    
    intentos = intentos + 1
    
    si tu_numero es igual a mi_numero_secreto
        decir "🎉 ¡GANASTE!"
        decir "Lo lograste en " + intentos + " intentos"
        salir del repetir
    si no
        si tu_numero es menor que mi_numero_secreto
            decir "📈 Mi número es más GRANDE"
        si no
            decir "📉 Mi número es más PEQUEÑO"
        terminar
        decir "¡Inténtalo otra vez!"
    terminar
terminar
```

### 🏪 **Tienda Virtual:**
```vader
tipo de cosa llamada Producto
    guardar nombre
    guardar precio
    guardar cantidad
    
    hacer mostrar_info
        decir "📦 " + self.nombre
        decir "💰 Precio: $" + self.precio
        decir "📊 Disponibles: " + self.cantidad
    terminar
terminar

# Crear productos
manzanas = Producto()
manzanas.nombre = "Manzanas"
manzanas.precio = 2
manzanas.cantidad = 50

peras = Producto()
peras.nombre = "Peras"
peras.precio = 3
peras.cantidad = 30

# Mostrar la tienda
decir "🏪 ¡Bienvenido a mi tienda!"
llamar manzanas.mostrar_info()
llamar peras.mostrar_info()

# Hacer una venta
preguntar "¿Qué quieres comprar?"
guardar la respuesta en producto_elegido

preguntar "¿Cuántos quieres?"
guardar la respuesta en cantidad_elegida
convertir cantidad_elegida a número

si producto_elegido es igual a "manzanas"
    total = manzanas.precio * cantidad_elegida
    decir "💰 Total a pagar: $" + total
    decir "¡Gracias por tu compra!"
si no
    si producto_elegido es igual a "peras"
        total = peras.precio * cantidad_elegida
        decir "💰 Total a pagar: $" + total
        decir "¡Gracias por tu compra!"
    si no
        decir "❌ No tenemos ese producto"
    terminar
terminar
```

---

## 🏠 Programas Útiles para Casa

### 📝 **Lista de Compras Inteligente:**
```vader
hacer agregar_a_lista con producto y lista
    agregar producto a lista
    decir "✅ Agregado: " + producto
    devolver lista
terminar

hacer mostrar_lista con lista
    si lista está vacía
        decir "📭 Tu lista está vacía"
    si no
        decir "🛒 Tu lista de compras:"
        repetir con cada cosa en lista
            decir "- " + cosa
        terminar
    terminar
terminar

# Usar el programa
mi_lista = []
decir "📝 Organizador de compras familiar"

repetir siempre
    preguntar "¿Qué necesitas comprar? (o 'ver' para ver la lista, 'listo' para terminar)"
    guardar la respuesta en comando
    
    si comando es igual a "listo"
        salir del repetir
    si comando es igual a "ver"
        llamar mostrar_lista(mi_lista)
    si no
        mi_lista = agregar_a_lista(comando, mi_lista)
    terminar
terminar

decir "🎉 ¡Lista completada!"
llamar mostrar_lista(mi_lista)
```

### 💰 **Administrador de Dinero:**
```vader
tipo de cosa llamada CuentaBanco
    guardar saldo
    guardar nombre_titular
    
    hacer depositar con cantidad
        self.saldo = self.saldo + cantidad
        decir "💰 Depositaste $" + cantidad
        decir "💳 Nuevo saldo: $" + self.saldo
    terminar
    
    hacer retirar con cantidad
        si cantidad es menor o igual que self.saldo
            self.saldo = self.saldo - cantidad
            decir "💸 Retiraste $" + cantidad
            decir "💳 Nuevo saldo: $" + self.saldo
        si no
            decir "❌ No tienes suficiente dinero"
            decir "💳 Tu saldo actual es: $" + self.saldo
        terminar
    terminar
    
    hacer mostrar_saldo
        decir "👤 Cuenta de: " + self.nombre_titular
        decir "💳 Saldo actual: $" + self.saldo
    terminar
terminar

# Crear cuenta
mi_cuenta = CuentaBanco()
mi_cuenta.nombre_titular = "Mi Familia"
mi_cuenta.saldo = 1000

decir "🏦 Bienvenido al banco familiar"
llamar mi_cuenta.mostrar_saldo()

repetir siempre
    decir "\n¿Qué quieres hacer?"
    decir "1. Ver saldo"
    decir "2. Depositar dinero"
    decir "3. Retirar dinero"
    decir "4. Salir"
    
    preguntar "Elige 1, 2, 3 o 4:"
    guardar la respuesta en opcion
    
    si opcion es igual a "1"
        llamar mi_cuenta.mostrar_saldo()
    si opcion es igual a "2"
        preguntar "¿Cuánto quieres depositar?"
        guardar la respuesta en cantidad
        convertir cantidad a número
        llamar mi_cuenta.depositar(cantidad)
    si opcion es igual a "3"
        preguntar "¿Cuánto quieres retirar?"
        guardar la respuesta en cantidad
        convertir cantidad a número
        llamar mi_cuenta.retirar(cantidad)
    si opcion es igual a "4"
        decir "👋 ¡Gracias por usar el banco familiar!"
        salir del repetir
    terminar
terminar
```

---

## 🎓 Para Estudiantes

### 📚 **Organizador de Tareas Escolares:**
```vader
tipo de cosa llamada Tarea
    guardar materia
    guardar descripcion
    guardar fecha_entrega
    guardar completada
    
    hacer mostrar
        estado = "✅" si self.completada si no "⏳"
        decir estado + " " + self.materia + ": " + self.descripcion
        decir "   📅 Entregar: " + self.fecha_entrega
    terminar
    
    hacer marcar_completada
        self.completada = sí
        decir "🎉 ¡Tarea completada: " + self.descripcion + "!"
    terminar
terminar

hacer crear_tarea con materia y descripcion y fecha
    nueva_tarea = Tarea()
    nueva_tarea.materia = materia
    nueva_tarea.descripcion = descripcion
    nueva_tarea.fecha_entrega = fecha
    nueva_tarea.completada = no
    devolver nueva_tarea
terminar

# Programa principal
mis_tareas = []
decir "📚 Organizador escolar súper fácil"

repetir siempre
    decir "\n¿Qué quieres hacer?"
    decir "1. Agregar tarea"
    decir "2. Ver todas las tareas"
    decir "3. Marcar tarea como completada"
    decir "4. Salir"
    
    preguntar "Elige una opción:"
    guardar la respuesta en opcion
    
    si opcion es igual a "1"
        preguntar "¿Qué materia?"
        guardar la respuesta en materia
        preguntar "¿Qué tarea es?"
        guardar la respuesta en descripcion
        preguntar "¿Cuándo se entrega?"
        guardar la respuesta en fecha
        
        nueva_tarea = crear_tarea(materia, descripcion, fecha)
        agregar nueva_tarea a mis_tareas
        decir "✅ Tarea agregada"
    
    si opcion es igual a "2"
        si mis_tareas está vacía
            decir "📭 No tienes tareas pendientes"
        si no
            decir "📋 Tus tareas:"
            repetir con cada tarea en mis_tareas
                llamar tarea.mostrar()
            terminar
        terminar
    
    si opcion es igual a "3"
        preguntar "¿Qué tarea completaste? (escribe la descripción)"
        guardar la respuesta en tarea_completada
        
        repetir con cada tarea en mis_tareas
            si tarea.descripcion es igual a tarea_completada
                llamar tarea.marcar_completada()
            terminar
        terminar
    
    si opcion es igual a "4"
        decir "🎓 ¡Que tengas éxito en tus estudios!"
        salir del repetir
    terminar
terminar
```

---

## 🌟 ¡Lo Lograste!

**¡Felicidades!** Ahora puedes programar en Vader usando español completamente natural. No necesitas memorizar comandos raros ni sintaxis complicada.

### 🎯 **Recuerda:**
- **Habla normal**: Escribe como le hablarías a un amigo
- **Sé específico**: Di exactamente lo que quieres que haga
- **Usa palabras simples**: "decir" en lugar de "print", "preguntar" en lugar de "input"
- **Piensa paso a paso**: Divide lo que quieres hacer en pasos pequeños

### 🚀 **Próximos pasos:**
1. **Practica** con los ejemplos de arriba
2. **Experimenta** creando tus propios programas
3. **Diviértete** - programar debe ser como jugar
4. **Comparte** tus creaciones con familia y amigos

---

<div align="center">

## 🎉 ¡Bienvenido al Futuro de la Programación!

**Con Vader, cualquier persona puede crear software increíble**

*"Programar nunca había sido tan fácil como hablar"*

</div>
