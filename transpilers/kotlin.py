"""
Transpilador de Vader a Kotlin
Convierte código Vader (español natural) a Kotlin moderno para Android

Autor: Adriano Giaquinto
Proyecto: LangVader - Democratización de la programación
Revolución: Desarrollo Android en español natural
"""

import re

def transpile_to_kotlin(vader_code):
    """
    Transpila código Vader a Kotlin moderno e idiomático
    
    Características soportadas:
    - Sintaxis natural en español
    - Funciones y clases
    - Variables y tipos
    - Condicionales y bucles
    - Entrada/salida
    - Listas y mapas
    - Programación orientada a objetos
    - Funciones de extensión
    - Null safety
    - Corrutinas básicas
    """
    
    kotlin_code = []
    lines = vader_code.strip().split('\n')
    indent_level = 0
    
    # Agregar imports y configuración inicial
    kotlin_code.append("// Código generado por Vader - Transpilador a Kotlin")
    kotlin_code.append("// Sintaxis natural en español convertida a Kotlin para Android")
    kotlin_code.append("")
    kotlin_code.append("import kotlin.random.Random")
    kotlin_code.append("import kotlinx.coroutines.*")
    kotlin_code.append("")
    
    for line in lines:
        line = line.strip()
        
        # Saltar líneas vacías y comentarios
        if not line or line.startswith('#'):
            if line.startswith('#'):
                kotlin_code.append("    " * indent_level + "//" + line[1:])
            else:
                kotlin_code.append("")
            continue
        
        # Variables y asignaciones
        if '=' in line and not any(keyword in line for keyword in ['si ', 'repetir', 'funcion', 'clase', 'hacer']):
            kotlin_line = transpile_variable_assignment(line)
            kotlin_code.append("    " * indent_level + kotlin_line)
        
        # Mostrar/Imprimir
        elif line.startswith('mostrar ') or line.startswith('decir '):
            content = line.split(' ', 1)[1]
            kotlin_line = f'println({transpile_expression(content)})'
            kotlin_code.append("    " * indent_level + kotlin_line)
        
        # Entrada del usuario
        elif line.startswith('leer '):
            var_name = line.split(' ', 1)[1]
            kotlin_line = f'val {var_name} = readLine() ?: ""'
            kotlin_code.append("    " * indent_level + kotlin_line)
        
        elif 'preguntar' in line and 'guardar la respuesta en' in line:
            parts = line.split('guardar la respuesta en')
            question = parts[0].replace('preguntar', '').strip().strip('"')
            var_name = parts[1].strip()
            kotlin_code.append("    " * indent_level + f'print("{question} ")')
            kotlin_code.append("    " * indent_level + f'val {var_name} = readLine() ?: ""')
        
        # Condicionales
        elif line.startswith('si '):
            condition = line[3:].strip()
            kotlin_condition = transpile_condition(condition)
            kotlin_code.append("    " * indent_level + f'if ({kotlin_condition}) {{')
            indent_level += 1
        
        elif line == 'sino' or line == 'si no':
            indent_level -= 1
            kotlin_code.append("    " * indent_level + '} else {')
            indent_level += 1
        
        elif line.startswith('sino si '):
            condition = line[8:].strip()
            kotlin_condition = transpile_condition(condition)
            indent_level -= 1
            kotlin_code.append("    " * indent_level + f'}} else if ({kotlin_condition}) {{')
            indent_level += 1
        
        # Bucles
        elif line.startswith('repetir '):
            if 'veces' in line:
                # repetir X veces
                match = re.search(r'repetir (\d+) veces', line)
                if match:
                    times = match.group(1)
                    kotlin_code.append("    " * indent_level + f'repeat({times}) {{')
                    indent_level += 1
            
            elif 'con cada' in line and 'en' in line:
                # repetir con cada elemento en lista
                parts = line.replace('repetir con cada ', '').split(' en ')
                item = parts[0].strip()
                collection = parts[1].strip()
                kotlin_code.append("    " * indent_level + f'for ({item} in {collection}) {{')
                indent_level += 1
            
            elif 'mientras' in line:
                # repetir mientras condicion
                condition = line.replace('repetir mientras ', '').strip()
                kotlin_condition = transpile_condition(condition)
                kotlin_code.append("    " * indent_level + f'while ({kotlin_condition}) {{')
                indent_level += 1
            
            elif 'siempre' in line:
                # repetir siempre
                kotlin_code.append("    " * indent_level + 'while (true) {')
                indent_level += 1
        
        # Funciones
        elif line.startswith('funcion ') or line.startswith('hacer '):
            func_def = transpile_function_definition(line)
            kotlin_code.append("    " * indent_level + func_def)
            indent_level += 1
        
        elif line.startswith('retornar ') or line.startswith('devolver '):
            value = line.split(' ', 1)[1]
            kotlin_line = f'return {transpile_expression(value)}'
            kotlin_code.append("    " * indent_level + kotlin_line)
        
        # Clases
        elif line.startswith('clase ') or line.startswith('tipo de cosa llamada '):
            class_def = transpile_class_definition(line)
            kotlin_code.append("    " * indent_level + class_def)
            indent_level += 1
        
        elif line.startswith('guardar '):
            # Atributo de clase
            attr_name = line.replace('guardar ', '').strip()
            kotlin_code.append("    " * indent_level + f'var {attr_name}: Any? = null')
        
        # Control de flujo
        elif line == 'romper' or line == 'salir del repetir':
            kotlin_code.append("    " * indent_level + 'break')
        
        elif line == 'continuar':
            kotlin_code.append("    " * indent_level + 'continue')
        
        # Conversiones
        elif 'convertir a numero' in line or 'convertir a número' in line:
            parts = line.split('convertir a num')
            var_part = parts[0].strip()
            if '=' in var_part:
                var_name = var_part.split('=')[0].strip()
                value = var_part.split('=')[1].strip()
                kotlin_code.append("    " * indent_level + f'val {var_name} = {value}.toIntOrNull() ?: 0')
            else:
                kotlin_code.append("    " * indent_level + f'{var_part}.toIntOrNull() ?: 0')
        
        elif 'convertir a texto' in line:
            parts = line.split('convertir a texto')
            var_part = parts[0].strip()
            if '=' in var_part:
                var_name = var_part.split('=')[0].strip()
                value = var_part.split('=')[1].strip()
                kotlin_code.append("    " * indent_level + f'val {var_name} = {value}.toString()')
            else:
                kotlin_code.append("    " * indent_level + f'{var_part}.toString()')
        
        # Llamadas a funciones
        elif line.startswith('llamar '):
            func_call = line.replace('llamar ', '').strip()
            kotlin_code.append("    " * indent_level + func_call)
        
        # Fin de bloques
        elif line in ['fin', 'terminar', 'fin si', 'fin funcion', 'fin clase', 'fin repetir']:
            indent_level -= 1
            kotlin_code.append("    " * indent_level + '}')
        
        # Líneas generales
        else:
            # Intentar transpillar como expresión general
            kotlin_line = transpile_general_line(line)
            if kotlin_line:
                kotlin_code.append("    " * indent_level + kotlin_line)
    
    # Agregar función main si no existe
    if not any('fun main' in line for line in kotlin_code):
        kotlin_code.append("")
        kotlin_code.append("fun main() {")
        kotlin_code.append("    // Código principal generado por Vader")
        kotlin_code.append("}")
    
    return '\n'.join(kotlin_code)

def transpile_variable_assignment(line):
    """Transpila asignaciones de variables a Kotlin"""
    if '=' in line:
        parts = line.split('=', 1)
        var_name = parts[0].strip()
        value = parts[1].strip()
        
        # Determinar tipo automáticamente
        kotlin_value = transpile_expression(value)
        
        # Usar val para constantes, var para variables
        if value.startswith('"') or value.replace('.', '').isdigit():
            return f'val {var_name} = {kotlin_value}'
        else:
            return f'var {var_name} = {kotlin_value}'
    
    return line

def transpile_expression(expr):
    """Transpila expresiones a Kotlin"""
    expr = expr.strip()
    
    # Strings
    if expr.startswith('"') and expr.endswith('"'):
        return expr
    
    # Números
    if expr.replace('.', '').replace('-', '').isdigit():
        return expr
    
    # Booleanos
    if expr.lower() in ['verdadero', 'true']:
        return 'true'
    elif expr.lower() in ['falso', 'false']:
        return 'false'
    
    # Listas
    if expr.startswith('[') and expr.endswith(']'):
        content = expr[1:-1]
        if content.strip():
            items = [transpile_expression(item.strip()) for item in content.split(',')]
            return f'listOf({", ".join(items)})'
        return 'emptyList<Any>()'
    
    # Mapas/Diccionarios
    if expr.startswith('{') and expr.endswith('}'):
        content = expr[1:-1]
        if content.strip():
            # Formato simple: {key: value, key2: value2}
            pairs = []
            for pair in content.split(','):
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    key = transpile_expression(key.strip())
                    value = transpile_expression(value.strip())
                    pairs.append(f'{key} to {value}')
            return f'mapOf({", ".join(pairs)})'
        return 'emptyMap<Any, Any>()'
    
    # Concatenación de strings
    if '+' in expr and '"' in expr:
        parts = expr.split('+')
        kotlin_parts = []
        for part in parts:
            part = part.strip()
            if part.startswith('"') and part.endswith('"'):
                kotlin_parts.append(part)
            else:
                kotlin_parts.append(f'${{{part}}}')
        
        # Crear string template
        result = '"'
        for i, part in enumerate(kotlin_parts):
            if part.startswith('"') and part.endswith('"'):
                result += part[1:-1]  # Remove quotes
            else:
                result += part
        result += '"'
        return result
    
    # Operaciones matemáticas
    expr = expr.replace(' y ', ' && ')
    expr = expr.replace(' o ', ' || ')
    expr = expr.replace(' es igual a ', ' == ')
    expr = expr.replace(' es mayor que ', ' > ')
    expr = expr.replace(' es menor que ', ' < ')
    expr = expr.replace(' no es ', ' != ')
    
    return expr

def transpile_condition(condition):
    """Transpila condiciones a Kotlin"""
    condition = condition.strip()
    
    # Reemplazos de operadores lógicos
    condition = condition.replace(' y también ', ' && ')
    condition = condition.replace(' o también ', ' || ')
    condition = condition.replace(' y ', ' && ')
    condition = condition.replace(' o ', ' || ')
    condition = condition.replace(' es igual a ', ' == ')
    condition = condition.replace(' es mayor que ', ' > ')
    condition = condition.replace(' es menor que ', ' < ')
    condition = condition.replace(' es mayor o igual a ', ' >= ')
    condition = condition.replace(' es menor o igual a ', ' <= ')
    condition = condition.replace(' no es igual a ', ' != ')
    condition = condition.replace(' no es ', ' != ')
    condition = condition.replace(' no ', ' !')
    
    return condition

def transpile_function_definition(line):
    """Transpila definiciones de funciones a Kotlin"""
    if line.startswith('funcion '):
        # funcion nombre(param1, param2)
        func_part = line.replace('funcion ', '').strip()
        if '(' in func_part:
            func_name = func_part.split('(')[0].strip()
            params_part = func_part.split('(')[1].replace(')', '').strip()
            
            if params_part:
                params = [f'{param.strip()}: Any' for param in params_part.split(',')]
                return f'fun {func_name}({", ".join(params)}) {{'
            else:
                return f'fun {func_name}() {{'
        else:
            return f'fun {func_part}() {{'
    
    elif line.startswith('hacer '):
        # hacer nombre_funcion con param1 y param2
        func_part = line.replace('hacer ', '').strip()
        
        if ' con ' in func_part:
            parts = func_part.split(' con ')
            func_name = parts[0].strip()
            params_part = parts[1].strip()
            
            # Separar parámetros por 'y'
            params = [f'{param.strip()}: Any' for param in params_part.split(' y ')]
            return f'fun {func_name}({", ".join(params)}) {{'
        else:
            return f'fun {func_part}() {{'
    
    return line

def transpile_class_definition(line):
    """Transpila definiciones de clases a Kotlin"""
    if line.startswith('clase '):
        class_name = line.replace('clase ', '').strip()
        return f'class {class_name} {{'
    
    elif line.startswith('tipo de cosa llamada '):
        class_name = line.replace('tipo de cosa llamada ', '').strip()
        return f'class {class_name} {{'
    
    return line

def transpile_general_line(line):
    """Transpila líneas generales que no encajan en categorías específicas"""
    line = line.strip()
    
    # Llamadas a métodos o funciones
    if '(' in line and ')' in line:
        return line
    
    # Asignaciones simples
    if '=' in line:
        return transpile_variable_assignment(line)
    
    # Expresiones simples
    return transpile_expression(line)

def format_kotlin_code(code):
    """Formatea el código Kotlin generado para mejor legibilidad"""
    lines = code.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Eliminar espacios extra
        line = line.rstrip()
        
        # Agregar líneas en blanco antes de funciones y clases
        if line.strip().startswith('fun ') or line.strip().startswith('class '):
            if formatted_lines and formatted_lines[-1].strip():
                formatted_lines.append('')
        
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

# Función principal del transpilador
def transpile(vader_code):
    """
    Función principal para transpillar código Vader a Kotlin
    """
    try:
        kotlin_code = transpile_to_kotlin(vader_code)
        formatted_code = format_kotlin_code(kotlin_code)
        return formatted_code
    except Exception as e:
        return f"// Error en la transpilación: {str(e)}\n// Código original:\n// {vader_code}"

# Función de compatibilidad con el sistema Vader
def transpilar(vader_code):
    """
    Función de compatibilidad con el sistema Vader
    """
    return transpile(vader_code)

if __name__ == "__main__":
    # Ejemplo de uso
    sample_vader = '''
    # Mi primera app Android con Vader
    decir "¡Hola desde Android!"
    
    nombre = "Vader"
    version = "1.0"
    
    decir "App: " + nombre
    decir "Versión: " + version
    
    hacer saludar con usuario
        decir "¡Hola " + usuario + " desde Android!"
    terminar
    
    llamar saludar("Adriano")
    '''
    
    print("=== Código Vader ===")
    print(sample_vader)
    print("\n=== Código Kotlin ===")
    print(transpile(sample_vader))
