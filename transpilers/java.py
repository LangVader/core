# Transpilador de Vader a Java
# Convierte código Vader en español a Java ejecutable

import re

def transpilar(codigo):
    """
    Transpila código Vader a Java
    """
    lineas = codigo.split('\n')
    resultado = []
    
    # Variables de estado para el transpilador
    en_clase = False
    en_funcion = False
    en_metodo = False
    nivel_indentacion = 0
    imports_necesarios = set()
    clase_principal = None
    tiene_main = False
    
    # Agregar imports básicos
    resultado.append("import java.util.*;")
    resultado.append("import java.io.*;")
    resultado.append("import java.lang.*;")
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
            # Agregar método main si no existe
            if clase_principal and not tiene_main:
                resultado.append("    public static void main(String[] args) {")
                resultado.append("        // Código principal aquí")
                resultado.append("    }")
        elif linea.startswith('funcion ') or linea.startswith('metodo '):
            en_funcion = True
            en_metodo = linea.startswith('metodo ')
        elif linea.startswith('fin funcion') or linea.startswith('fin metodo'):
            en_funcion = False
            en_metodo = False
        elif 'main(' in linea:
            tiene_main = True
        
        resultado.append(linea_transpilada)
        i += 1
    
    # Si no hay clase principal, crear una
    if not clase_principal:
        codigo_java = []
        codigo_java.extend(resultado[:4])  # Imports
        codigo_java.append("public class VaderProgram {")
        codigo_java.append("    public static void main(String[] args) {")
        
        # Agregar el código transpilado con indentación
        for linea in resultado[4:]:
            if linea.strip():
                codigo_java.append("        " + linea)
            else:
                codigo_java.append("")
        
        codigo_java.append("    }")
        codigo_java.append("}")
        return '\n'.join(codigo_java)
    
    return '\n'.join(resultado)

def transpilar_linea(linea, en_clase, en_funcion, en_metodo):
    """
    Transpila una línea individual de Vader a Java
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
    return f"public class {nombre} {{"

def transpilar_herencia(linea):
    """Transpila herencia de clases"""
    partes = linea.split(' hereda ')
    clase = partes[0].replace('clase ', '').strip()
    padre = partes[1].strip()
    return f"public class {clase} extends {padre} {{"

def transpilar_metodo_funcion(linea, en_clase):
    """Transpila métodos y funciones"""
    # Extraer nombre y parámetros
    if linea.startswith('metodo '):
        definicion = linea.replace('metodo ', '').strip()
        if en_clase:
            if definicion.startswith('__init__'):
                return transpilar_constructor(linea)
            else:
                return f"    public void {convertir_definicion_metodo(definicion)} {{"
        else:
            return f"public void {convertir_definicion_metodo(definicion)} {{"
    else:  # funcion
        definicion = linea.replace('funcion ', '').strip()
        if en_clase:
            return f"    public static void {convertir_definicion_metodo(definicion)} {{"
        else:
            return f"public static void {convertir_definicion_metodo(definicion)} {{"

def transpilar_constructor(linea):
    """Transpila constructor de clase"""
    # Extraer parámetros del constructor
    match = re.search(r'__init__\((.*?)\)', linea)
    if match:
        params = match.group(1)
        # Remover 'self' de los parámetros
        params_sin_self = ', '.join([p.strip() for p in params.split(',') if p.strip() != 'self'])
        return f"    public ClassName({params_sin_self}) {{"
    return "    public ClassName() {"

def convertir_definicion_metodo(definicion):
    """Convierte definición de método Vader a Java"""
    if '(' in definicion:
        nombre = definicion.split('(')[0]
        params = definicion.split('(')[1].replace(')', '')
        # Remover 'self' de los parámetros
        if params:
            params_lista = [p.strip() for p in params.split(',') if p.strip() != 'self']
            params_java = ', '.join([f"Object {p}" for p in params_lista])
        else:
            params_java = ""
        return f"{nombre}({params_java})"
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
            return f"String {variable} = {valor};"
        elif valor.startswith('[') and valor.endswith(']'):
            return f"ArrayList<Object> {variable} = new ArrayList<>(Arrays.asList({valor.replace('[', '').replace(']', '')}));"
        elif valor.startswith('{') and valor.endswith('}'):
            return f"HashMap<String, Object> {variable} = new HashMap<>();"
        elif valor.isdigit():
            return f"int {variable} = {valor};"
        elif '.' in valor and valor.replace('.', '').isdigit():
            return f"double {variable} = {valor};"
        elif valor in ['True', 'False']:
            valor_java = valor.lower()
            return f"boolean {variable} = {valor_java};"
        else:
            return f"Object {variable} = {valor};"
    
    return linea + ";"

def transpilar_si(linea):
    """Transpila condicionales si"""
    condicion = linea.replace('si ', '').strip()
    condicion_java = convertir_condicion(condicion)
    return f"if ({condicion_java}) {{"

def transpilar_sino_si(linea):
    """Transpila sino si (else if)"""
    condicion = linea.replace('sino si ', '').strip()
    condicion_java = convertir_condicion(condicion)
    return f"}} else if ({condicion_java}) {{"

def convertir_condicion(condicion):
    """Convierte condiciones Vader a Java"""
    # Operadores lógicos
    condicion = condicion.replace(' y ', ' && ')
    condicion = condicion.replace(' o ', ' || ')
    condicion = condicion.replace(' no ', ' !')
    condicion = condicion.replace(' en ', '.contains(')
    
    # Si hay 'contains', cerrar paréntesis
    if '.contains(' in condicion:
        condicion += ')'
    
    return condicion

def transpilar_bucle(linea):
    """Transpila bucles repetir"""
    if 'desde' in linea and 'hasta' in linea:
        # repetir i desde 1 hasta 10
        match = re.search(r'repetir (\w+) desde (\d+) hasta (\d+)', linea)
        if match:
            var, inicio, fin = match.groups()
            return f"for (int {var} = {inicio}; {var} <= {fin}; {var}++) {{"
    
    elif 'mientras' in linea:
        # repetir mientras condicion
        condicion = linea.replace('repetir mientras ', '').strip()
        condicion_java = convertir_condicion(condicion)
        return f"while ({condicion_java}) {{"
    
    elif ' en ' in linea:
        # repetir item en lista
        match = re.search(r'repetir (\w+) en (\w+)', linea)
        if match:
            item, lista = match.groups()
            return f"for (Object {item} : {lista}) {{"
    
    return "// Bucle no reconocido"

def transpilar_mostrar(linea):
    """Transpila mostrar (print)"""
    contenido = linea.replace('mostrar ', '').strip()
    if contenido.startswith('"') and contenido.endswith('"'):
        return f"System.out.println({contenido});"
    else:
        # Manejar concatenación con +
        contenido_java = convertir_concatenacion(contenido)
        return f"System.out.println({contenido_java});"

def transpilar_leer(linea):
    """Transpila leer (input)"""
    variable = linea.replace('leer ', '').strip()
    return f"Scanner scanner = new Scanner(System.in);\nString {variable} = scanner.nextLine();"

def convertir_concatenacion(expresion):
    """Convierte concatenación Vader a Java"""
    # Reemplazar str() por String.valueOf()
    expresion = re.sub(r'str\((.*?)\)', r'String.valueOf(\1)', expresion)
    return expresion

def transpilar_capturar(linea):
    """Transpila capturar excepciones"""
    if ' como ' in linea:
        partes = linea.replace('capturar ', '').split(' como ')
        excepcion = partes[0].strip()
        variable = partes[1].strip()
        return f"}} catch ({excepcion} {variable}) {{"
    else:
        excepcion = linea.replace('capturar ', '').strip()
        return f"}} catch ({excepcion} e) {{"

def transpilar_lista(linea):
    """Transpila listas"""
    match = re.search(r'lista (\w+) = \[(.*?)\]', linea)
    if match:
        nombre, elementos = match.groups()
        return f"ArrayList<Object> {nombre} = new ArrayList<>(Arrays.asList({elementos}));"
    return linea + ";"

def transpilar_diccionario(linea):
    """Transpila diccionarios"""
    match = re.search(r'diccionario (\w+) = \{(.*?)\}', linea)
    if match:
        nombre, contenido = match.groups()
        return f"HashMap<String, Object> {nombre} = new HashMap<>();"
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

def optimizar_imports(codigo_java):
    """Optimiza los imports según el código generado"""
    imports_necesarios = set()
    
    if 'Scanner' in codigo_java:
        imports_necesarios.add('import java.util.Scanner;')
    if 'ArrayList' in codigo_java:
        imports_necesarios.add('import java.util.ArrayList;')
    if 'HashMap' in codigo_java:
        imports_necesarios.add('import java.util.HashMap;')
    if 'Arrays' in codigo_java:
        imports_necesarios.add('import java.util.Arrays;')
    
    return imports_necesarios

def validar_sintaxis_java(codigo_java):
    """Valida la sintaxis básica del código Java generado"""
    errores = []
    
    # Verificar balance de llaves
    abiertas = codigo_java.count('{')
    cerradas = codigo_java.count('}')
    if abiertas != cerradas:
        errores.append(f"Llaves desbalanceadas: {abiertas} abiertas, {cerradas} cerradas")
    
    # Verificar que hay al menos una clase
    if 'class ' not in codigo_java:
        errores.append("No se encontró definición de clase")
    
    return errores

def formatear_codigo_java(codigo_java):
    """Formatea el código Java para mejor legibilidad"""
    lineas = codigo_java.split('\n')
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
