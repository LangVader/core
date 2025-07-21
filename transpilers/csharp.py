# Transpilador de Vader a C#
# Convierte código Vader en español a C# ejecutable

import re

def transpilar(codigo):
    """
    Transpila código Vader a C#
    """
    lineas = codigo.split('\n')
    resultado = []
    
    # Variables de estado para el transpilador
    en_clase = False
    en_funcion = False
    en_metodo = False
    nivel_indentacion = 0
    using_necesarios = set()
    clase_principal = None
    tiene_main = False
    
    # Agregar using statements básicos
    resultado.append("using System;")
    resultado.append("using System.Collections.Generic;")
    resultado.append("using System.IO;")
    resultado.append("using System.Linq;")
    resultado.append("using System.Text;")
    resultado.append("")
    
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        # Saltar líneas vacías y comentarios
        if not linea or linea.startswith('#'):
            if linea.startswith('#'):
                resultado.append("// " + linea[1:].strip())
            else:
                resultado.append("")
            i += 1
            continue
        
        # Detectar y transpilar diferentes construcciones
        linea_transpilada = transpilar_linea(linea, en_clase, en_funcion, en_metodo)
        
        # Actualizar estado del transpilador
        if linea.startswith('clase '):
            en_clase = True
            clase_principal = extraer_nombre_clase(linea)
        elif linea.startswith('fin clase'):
            en_clase = False
            # Agregar método Main si no existe
            if clase_principal and not tiene_main:
                resultado.append("    static void Main(string[] args)")
                resultado.append("    {")
                resultado.append("        // Código principal aquí")
                resultado.append("    }")
        elif linea.startswith('funcion ') or linea.startswith('metodo '):
            en_funcion = True
            en_metodo = linea.startswith('metodo ')
        elif linea.startswith('fin funcion') or linea.startswith('fin metodo'):
            en_funcion = False
            en_metodo = False
        elif 'Main(' in linea:
            tiene_main = True
        
        resultado.append(linea_transpilada)
        i += 1
    
    # Si no hay clase principal, crear una
    if not clase_principal:
        codigo_csharp = []
        codigo_csharp.extend(resultado[:6])  # Using statements
        codigo_csharp.append("class VaderProgram")
        codigo_csharp.append("{")
        codigo_csharp.append("    static void Main(string[] args)")
        codigo_csharp.append("    {")
        
        # Agregar el código transpilado con indentación
        for linea in resultado[6:]:
            if linea.strip():
                codigo_csharp.append("        " + linea)
            else:
                codigo_csharp.append("")
        
        codigo_csharp.append("    }")
        codigo_csharp.append("}")
        return '\n'.join(codigo_csharp)
    
    return '\n'.join(resultado)

def transpilar_linea(linea, en_clase, en_funcion, en_metodo):
    """
    Transpila una línea individual de Vader a C#
    """
    linea = linea.strip()
    
    # Clases
    if linea.startswith('clase '):
        return transpilar_clase(linea)
    
    # Herencia
    if ' hereda ' in linea and linea.startswith('clase '):
        return transpilar_herencia(linea)
    
    # Métodos y funciones
    if linea.startswith('metodo ') or linea.startswith('funcion '):
        return transpilar_metodo_funcion(linea, en_clase)
    
    # Constructores
    if linea.startswith('metodo __init__'):
        return transpilar_constructor(linea)
    
    # Variables y asignaciones
    if '=' in linea and not any(op in linea for op in ['==', '!=', '<=', '>=']):
        return transpilar_asignacion(linea)
    
    # Estructuras de control
    if linea.startswith('si '):
        return transpilar_si(linea)
    elif linea.startswith('sino si '):
        return transpilar_sino_si(linea)
    elif linea.startswith('sino'):
        return "} else {"
    elif linea.startswith('fin si'):
        return "}"
    
    # Bucles
    if linea.startswith('repetir '):
        return transpilar_bucle(linea)
    elif linea.startswith('fin repetir'):
        return "}"
    
    # Entrada y salida
    if linea.startswith('mostrar '):
        return transpilar_mostrar(linea)
    elif linea.startswith('leer '):
        return transpilar_leer(linea)
    
    # Manejo de errores
    if linea.startswith('intentar'):
        return "try {"
    elif linea.startswith('capturar '):
        return transpilar_capturar(linea)
    elif linea.startswith('finalmente'):
        return "} finally {"
    elif linea.startswith('fin intentar'):
        return "}"
    
    # Listas y colecciones
    if linea.startswith('lista '):
        return transpilar_lista(linea)
    elif linea.startswith('diccionario '):
        return transpilar_diccionario(linea)
    
    # Control de flujo
    if linea.startswith('retornar '):
        return transpilar_retornar(linea)
    elif linea == 'romper':
        return "break;"
    elif linea == 'continuar':
        return "continue;"
    
    # Llamadas a funciones
    if linea.startswith('llamar '):
        return transpilar_llamada_funcion(linea)
    
    # Creación de objetos
    if linea.startswith('crear '):
        return transpilar_crear_objeto(linea)
    
    # Finalizadores
    if linea.startswith('fin '):
        return "}"
    
    # Línea genérica - intentar transpilación básica
    return transpilar_expresion_generica(linea)

def transpilar_clase(linea):
    """Transpila definición de clase"""
    nombre = linea.replace('clase ', '').strip()
    return f"public class {nombre}"

def transpilar_herencia(linea):
    """Transpila herencia de clases"""
    partes = linea.split(' hereda ')
    clase = partes[0].replace('clase ', '').strip()
    padre = partes[1].strip()
    return f"public class {clase} : {padre}"

def transpilar_metodo_funcion(linea, en_clase):
    """Transpila métodos y funciones"""
    # Extraer nombre y parámetros
    if linea.startswith('metodo '):
        definicion = linea.replace('metodo ', '').strip()
        if en_clase:
            if definicion.startswith('__init__'):
                return transpilar_constructor(linea)
            else:
                return f"    public void {convertir_definicion_metodo(definicion)}"
        else:
            return f"public void {convertir_definicion_metodo(definicion)}"
    else:  # funcion
        definicion = linea.replace('funcion ', '').strip()
        if en_clase:
            return f"    public static void {convertir_definicion_metodo(definicion)}"
        else:
            return f"public static void {convertir_definicion_metodo(definicion)}"

def transpilar_constructor(linea):
    """Transpila constructor de clase"""
    # Extraer parámetros del constructor
    match = re.search(r'__init__\((.*?)\)', linea)
    if match:
        params = match.group(1)
        # Remover 'self' de los parámetros
        params_sin_self = ', '.join([f"object {p.strip()}" for p in params.split(',') if p.strip() != 'self'])
        return f"    public ClassName({params_sin_self})"
    return "    public ClassName()"

def convertir_definicion_metodo(definicion):
    """Convierte definición de método Vader a C#"""
    if '(' in definicion:
        nombre = definicion.split('(')[0]
        params = definicion.split('(')[1].replace(')', '')
        # Remover 'self' de los parámetros
        if params:
            params_lista = [p.strip() for p in params.split(',') if p.strip() != 'self']
            params_csharp = ', '.join([f"object {p}" for p in params_lista])
        else:
            params_csharp = ""
        return f"{nombre}({params_csharp})"
    else:
        return f"{definicion}()"

def transpilar_asignacion(linea):
    """Transpila asignaciones de variables"""
    if '=' in linea:
        partes = linea.split('=', 1)
        variable = partes[0].strip()
        valor = partes[1].strip()
        
        # Detectar tipo de variable
        if valor.startswith('"') and valor.endswith('"'):
            return f"string {variable} = {valor};"
        elif valor.startswith('[') and valor.endswith(']'):
            elementos = valor.replace('[', '').replace(']', '')
            return f"List<object> {variable} = new List<object> {{ {elementos} }};"
        elif valor.startswith('{') and valor.endswith('}'):
            return f"Dictionary<string, object> {variable} = new Dictionary<string, object>();"
        elif valor.isdigit():
            return f"int {variable} = {valor};"
        elif '.' in valor and valor.replace('.', '').replace('-', '').isdigit():
            return f"double {variable} = {valor};"
        elif valor in ['True', 'False']:
            valor_csharp = valor.lower()
            return f"bool {variable} = {valor_csharp};"
        else:
            return f"var {variable} = {valor};"
    
    return linea + ";"

def transpilar_si(linea):
    """Transpila condicionales si"""
    condicion = linea.replace('si ', '').strip()
    condicion_csharp = convertir_condicion(condicion)
    return f"if ({condicion_csharp})"

def transpilar_sino_si(linea):
    """Transpila sino si (else if)"""
    condicion = linea.replace('sino si ', '').strip()
    condicion_csharp = convertir_condicion(condicion)
    return f"}} else if ({condicion_csharp})"

def convertir_condicion(condicion):
    """Convierte condiciones Vader a C#"""
    # Operadores lógicos
    condicion = condicion.replace(' y ', ' && ')
    condicion = condicion.replace(' o ', ' || ')
    condicion = condicion.replace(' no ', ' !')
    condicion = condicion.replace(' en ', '.Contains(')
    
    # Si hay 'Contains', cerrar paréntesis
    if '.Contains(' in condicion:
        condicion += ')'
    
    return condicion

def transpilar_bucle(linea):
    """Transpila bucles repetir"""
    if 'desde' in linea and 'hasta' in linea:
        # repetir i desde 1 hasta 10
        match = re.search(r'repetir (\w+) desde (\d+) hasta (\d+)', linea)
        if match:
            var, inicio, fin = match.groups()
            return f"for (int {var} = {inicio}; {var} <= {fin}; {var}++)"
    
    elif 'mientras' in linea:
        # repetir mientras condicion
        condicion = linea.replace('repetir mientras ', '').strip()
        condicion_csharp = convertir_condicion(condicion)
        return f"while ({condicion_csharp})"
    
    elif ' en ' in linea:
        # repetir item en lista
        match = re.search(r'repetir (\w+) en (\w+)', linea)
        if match:
            item, lista = match.groups()
            return f"foreach (var {item} in {lista})"
    
    return "// Bucle no reconocido"

def transpilar_mostrar(linea):
    """Transpila mostrar (print)"""
    contenido = linea.replace('mostrar ', '').strip()
    if contenido.startswith('"') and contenido.endswith('"'):
        return f"Console.WriteLine({contenido});"
    else:
        # Manejar concatenación con +
        contenido_csharp = convertir_concatenacion(contenido)
        return f"Console.WriteLine({contenido_csharp});"

def transpilar_leer(linea):
    """Transpila leer (input)"""
    variable = linea.replace('leer ', '').strip()
    return f"string {variable} = Console.ReadLine();"

def convertir_concatenacion(expresion):
    """Convierte concatenación Vader a C#"""
    # Reemplazar str() por .ToString()
    expresion = re.sub(r'str\((.*?)\)', r'(\1).ToString()', expresion)
    return expresion

def transpilar_capturar(linea):
    """Transpila capturar excepciones"""
    if ' como ' in linea:
        partes = linea.replace('capturar ', '').split(' como ')
        excepcion = partes[0].strip()
        variable = partes[1].strip()
        return f"}} catch ({excepcion} {variable})"
    else:
        excepcion = linea.replace('capturar ', '').strip()
        return f"}} catch ({excepcion} ex)"

def transpilar_lista(linea):
    """Transpila listas"""
    match = re.search(r'lista (\w+) = \[(.*?)\]', linea)
    if match:
        nombre, elementos = match.groups()
        return f"List<object> {nombre} = new List<object> {{ {elementos} }};"
    return linea + ";"

def transpilar_diccionario(linea):
    """Transpila diccionarios"""
    match = re.search(r'diccionario (\w+) = \{(.*?)\}', linea)
    if match:
        nombre, contenido = match.groups()
        return f"Dictionary<string, object> {nombre} = new Dictionary<string, object>();"
    return linea + ";"

def transpilar_retornar(linea):
    """Transpila return"""
    valor = linea.replace('retornar ', '').strip()
    return f"return {valor};"

def transpilar_llamada_funcion(linea):
    """Transpila llamadas a funciones"""
    llamada = linea.replace('llamar ', '').strip()
    return f"{llamada};"

def transpilar_crear_objeto(linea):
    """Transpila creación de objetos"""
    # crear objeto como Clase(params)
    match = re.search(r'crear (\w+) como (\w+)\((.*?)\)', linea)
    if match:
        variable, clase, params = match.groups()
        return f"{clase} {variable} = new {clase}({params});"
    return linea + ";"

def transpilar_expresion_generica(linea):
    """Transpila expresiones genéricas"""
    # Si la línea no termina en ; y no es una estructura de control, agregarla
    if not linea.endswith((';', '{', '}')):
        return linea + ";"
    return linea

def extraer_nombre_clase(linea):
    """Extrae el nombre de la clase de la definición"""
    if ' hereda ' in linea:
        return linea.split(' hereda ')[0].replace('clase ', '').strip()
    else:
        return linea.replace('clase ', '').strip()

# Funciones auxiliares para mejorar la transpilación

def optimizar_using(codigo_csharp):
    """Optimiza los using statements según el código generado"""
    using_necesarios = set()
    
    if 'Console' in codigo_csharp:
        using_necesarios.add('using System;')
    if 'List<' in codigo_csharp:
        using_necesarios.add('using System.Collections.Generic;')
    if 'Dictionary<' in codigo_csharp:
        using_necesarios.add('using System.Collections.Generic;')
    if 'File' in codigo_csharp:
        using_necesarios.add('using System.IO;')
    if 'Linq' in codigo_csharp:
        using_necesarios.add('using System.Linq;')
    
    return using_necesarios

def validar_sintaxis_csharp(codigo_csharp):
    """Valida la sintaxis básica del código C# generado"""
    errores = []
    
    # Verificar balance de llaves
    abiertas = codigo_csharp.count('{')
    cerradas = codigo_csharp.count('}')
    if abiertas != cerradas:
        errores.append(f"Llaves desbalanceadas: {abiertas} abiertas, {cerradas} cerradas")
    
    # Verificar que hay al menos una clase
    if 'class ' not in codigo_csharp:
        errores.append("No se encontró definición de clase")
    
    return errores

def formatear_codigo_csharp(codigo_csharp):
    """Formatea el código C# para mejor legibilidad"""
    lineas = codigo_csharp.split('\n')
    resultado = []
    nivel_indentacion = 0
    
    for linea in lineas:
        linea_limpia = linea.strip()
        
        # Reducir indentación antes de }
        if linea_limpia.startswith('}'):
            nivel_indentacion = max(0, nivel_indentacion - 1)
        
        # Agregar indentación
        if linea_limpia:
            resultado.append('    ' * nivel_indentacion + linea_limpia)
        else:
            resultado.append('')
        
        # Aumentar indentación después de {
        if linea_limpia.endswith('{'):
            nivel_indentacion += 1
    
    return '\n'.join(resultado)

# Funciones específicas para características avanzadas de C#

def transpilar_propiedades(linea):
    """Transpila propiedades de C#"""
    # propiedad Nombre como string
    match = re.search(r'propiedad (\w+) como (\w+)', linea)
    if match:
        nombre, tipo = match.groups()
        return f"public {tipo} {nombre} {{ get; set; }}"
    return linea

def transpilar_eventos(linea):
    """Transpila eventos de C#"""
    # evento OnClick como EventHandler
    match = re.search(r'evento (\w+) como (\w+)', linea)
    if match:
        nombre, tipo = match.groups()
        return f"public event {tipo} {nombre};"
    return linea

def transpilar_async_await(linea):
    """Transpila async/await de C#"""
    if linea.startswith('asincrona funcion '):
        definicion = linea.replace('asincrona funcion ', '').strip()
        return f"public async Task {convertir_definicion_metodo(definicion)}"
    elif linea.startswith('esperar '):
        expresion = linea.replace('esperar ', '').strip()
        return f"await {expresion};"
    return linea

def transpilar_linq(linea):
    """Transpila operaciones LINQ básicas"""
    # Ejemplo: filtrar lista donde item > 5
    if 'filtrar' in linea and 'donde' in linea:
        match = re.search(r'filtrar (\w+) donde (.*)', linea)
        if match:
            lista, condicion = match.groups()
            return f"{lista}.Where(item => {condicion})"
    return linea

def transpilar_interfaces(linea):
    """Transpila interfaces"""
    if linea.startswith('interfaz '):
        nombre = linea.replace('interfaz ', '').strip()
        return f"public interface {nombre}"
    return linea

def transpilar_genericos(linea):
    """Transpila genéricos básicos"""
    # clase Lista<T>
    if '<' in linea and '>' in linea and linea.startswith('clase '):
        return linea.replace('clase ', 'public class ')
    return linea
