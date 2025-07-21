"""
Transpilador de Vader a Swift
Convierte código Vader (español natural) a código Swift idiomático para iOS/macOS
"""

import re

def transpilar(codigo):
    """
    Transpila código Vader a Swift
    Soporta sintaxis natural en español y genera código Swift moderno y eficiente
    """
    
    # Inicializar el código Swift
    swift_code = []
    
    # Headers y imports necesarios
    swift_code.append("// Código generado por Vader - Transpilador a Swift")
    swift_code.append("// Sintaxis natural en español convertida a Swift para iOS/macOS")
    swift_code.append("")
    
    # Imports comunes de Swift
    imports_needed = set()
    imports_needed.add("import Foundation")
    
    # Dividir en líneas y procesar
    lineas = codigo.strip().split('\n')
    indent_level = 0
    in_function = False
    in_class = False
    in_struct = False
    current_class = ""
    
    # Variables para tracking
    variables_declared = set()
    functions_declared = set()
    classes_declared = set()
    
    for i, linea in enumerate(lineas):
        linea_original = linea
        linea = linea.strip()
        
        # Saltar líneas vacías y comentarios
        if not linea or linea.startswith('#'):
            if linea.startswith('#'):
                swift_code.append("    " * indent_level + "//" + linea[1:])
            else:
                swift_code.append("")
            continue
        
        # SINTAXIS NATURAL - Mostrar/Decir
        if linea.startswith('decir ') or linea.startswith('mostrar '):
            content = linea.split(' ', 1)[1]
            # Manejar concatenación de strings
            if ' + ' in content:
                parts = content.split(' + ')
                formatted_parts = []
                for part in parts:
                    part = part.strip()
                    if part.startswith('"') and part.endswith('"'):
                        formatted_parts.append(part)
                    else:
                        formatted_parts.append(f"\\({part})")
                swift_content = f'print("{"".join(formatted_parts)}")'
            else:
                if content.startswith('"') and content.endswith('"'):
                    swift_content = f'print({content})'
                else:
                    swift_content = f'print("\\({content})")'
            swift_code.append("    " * indent_level + swift_content)
            continue
        
        # SINTAXIS NATURAL - Preguntar y guardar respuesta
        if linea.startswith('preguntar ') and ' guardar la respuesta en ' in linea:
            parts = linea.split(' guardar la respuesta en ')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            
            if question.startswith('"') and question.endswith('"'):
                clean_question = question[1:-1]
            else:
                clean_question = question
            
            swift_code.append("    " * indent_level + f'print("{clean_question}")')
            swift_code.append("    " * indent_level + f'let {var_name} = readLine() ?? ""')
            variables_declared.add(var_name)
            continue
        
        # SINTAXIS NATURAL - Conversiones
        if 'convertir a número' in linea:
            parts = linea.split(' = ')
            if len(parts) == 2:
                var_name = parts[0].strip()
                conversion = parts[1].replace('convertir a número', '').strip()
                swift_code.append("    " * indent_level + f'let {var_name} = Int({conversion}) ?? 0')
                variables_declared.add(var_name)
            continue
        
        if 'convertir a texto' in linea:
            parts = linea.split(' = ')
            if len(parts) == 2:
                var_name = parts[0].strip()
                conversion = parts[1].replace('convertir a texto', '').strip()
                swift_code.append("    " * indent_level + f'let {var_name} = String({conversion})')
                variables_declared.add(var_name)
            continue
        
        # SINTAXIS NATURAL - Definir funciones
        if linea.startswith('hacer ') and (' con ' in linea or linea.endswith('hacer')):
            if ' con ' in linea:
                parts = linea.replace('hacer ', '').split(' con ')
                func_name = parts[0].strip()
                params = parts[1].strip().replace(' y ', ', ')
                # Convertir parámetros a formato Swift
                swift_params = []
                for param in params.split(', '):
                    param = param.strip()
                    swift_params.append(f'{param}: String')
                swift_code.append("    " * indent_level + f'func {func_name}({", ".join(swift_params)}) {{')
            else:
                func_name = linea.replace('hacer ', '').strip()
                swift_code.append("    " * indent_level + f'func {func_name}() {{')
            
            functions_declared.add(func_name)
            indent_level += 1
            in_function = True
            continue
        
        # SINTAXIS NATURAL - Definir clases/structs
        if linea.startswith('tipo de cosa llamada '):
            class_name = linea.replace('tipo de cosa llamada ', '').strip()
            if ' hereda ' in class_name:
                parts = class_name.split(' hereda ')
                class_name = parts[0].strip()
                parent_class = parts[1].strip()
                swift_code.append("    " * indent_level + f'class {class_name}: {parent_class} {{')
                in_class = True
            else:
                swift_code.append("    " * indent_level + f'struct {class_name} {{')
                in_struct = True
            
            current_class = class_name
            classes_declared.add(class_name)
            indent_level += 1
            continue
        
        # SINTAXIS NATURAL - Propiedades de clase/struct
        if linea.startswith('guardar ') and (in_class or in_struct):
            prop_name = linea.replace('guardar ', '').strip()
            swift_code.append("    " * indent_level + f'var {prop_name}: String = ""')
            continue
        
        # SINTAXIS NATURAL - Devolver
        if linea.startswith('devolver '):
            value = linea.replace('devolver ', '').strip()
            swift_code.append("    " * indent_level + f'return {value}')
            continue
        
        # SINTAXIS NATURAL - Condicionales
        if linea.startswith('si '):
            condition = linea.replace('si ', '').strip()
            # Convertir comparaciones naturales
            condition = condition.replace(' es igual a ', ' == ')
            condition = condition.replace(' es mayor que ', ' > ')
            condition = condition.replace(' es menor que ', ' < ')
            condition = condition.replace(' y también ', ' && ')
            condition = condition.replace(' o también ', ' || ')
            
            swift_code.append("    " * indent_level + f'if {condition} {{')
            indent_level += 1
            continue
        
        if linea == 'si no':
            indent_level -= 1
            swift_code.append("    " * indent_level + '} else {')
            indent_level += 1
            continue
        
        # SINTAXIS NATURAL - Bucles
        if linea.startswith('repetir ') and ' veces' in linea:
            times = linea.replace('repetir ', '').replace(' veces', '').strip()
            swift_code.append("    " * indent_level + f'for _ in 0..<{times} {{')
            indent_level += 1
            continue
        
        if linea.startswith('repetir con cada ') and ' en ' in linea:
            parts = linea.replace('repetir con cada ', '').split(' en ')
            item = parts[0].strip()
            collection = parts[1].strip()
            swift_code.append("    " * indent_level + f'for {item} in {collection} {{')
            indent_level += 1
            continue
        
        if linea.startswith('repetir siempre'):
            swift_code.append("    " * indent_level + 'while true {')
            indent_level += 1
            continue
        
        if linea == 'salir del repetir':
            swift_code.append("    " * indent_level + 'break')
            continue
        
        # SINTAXIS NATURAL - Terminar bloques
        if linea == 'terminar':
            indent_level -= 1
            swift_code.append("    " * indent_level + '}')
            if in_function:
                in_function = False
            elif in_class:
                in_class = False
            elif in_struct:
                in_struct = False
            continue
        
        # Variables y asignaciones
        if ' = ' in linea and not linea.startswith('si '):
            parts = linea.split(' = ', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            
            # Detectar tipo de dato
            if value.startswith('"') and value.endswith('"'):
                swift_code.append("    " * indent_level + f'let {var_name} = {value}')
            elif value.startswith('[') and value.endswith(']'):
                swift_code.append("    " * indent_level + f'let {var_name} = {value}')
            elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                swift_code.append("    " * indent_level + f'let {var_name} = {value}')
            elif value in ['true', 'false', 'sí', 'no']:
                bool_value = 'true' if value in ['true', 'sí'] else 'false'
                swift_code.append("    " * indent_level + f'let {var_name} = {bool_value}')
            else:
                swift_code.append("    " * indent_level + f'let {var_name} = {value}')
            
            variables_declared.add(var_name)
            continue
        
        # Llamadas a funciones
        if linea.startswith('llamar '):
            func_call = linea.replace('llamar ', '').strip()
            if '(' not in func_call:
                func_call += '()'
            swift_code.append("    " * indent_level + f'{func_call}')
            continue
        
        # Líneas que no coinciden con patrones específicos
        swift_code.append("    " * indent_level + f'// TODO: {linea}')
    
    # Agregar función main si es necesario (para apps de consola)
    if not any('class' in line or 'struct' in line for line in swift_code):
        # Es una app de consola, agregar función main
        swift_code.append("")
        swift_code.append("// Función principal")
        swift_code.append("func main() {")
        swift_code.append("    // Código principal aquí")
        swift_code.append("}")
        swift_code.append("")
        swift_code.append("main()")
    
    # Agregar imports al inicio
    if imports_needed:
        final_code = list(imports_needed) + [""] + swift_code
    else:
        final_code = swift_code
    
    return '\n'.join(final_code)

def format_swift_code(code):
    """
    Formatea el código Swift generado para mejor legibilidad
    """
    lines = code.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Limpiar espacios extra
        line = line.rstrip()
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

# Función principal de transpilación
def transpilar_a_swift(codigo_vader):
    """
    Función principal que transpila código Vader a Swift
    """
    codigo_swift = transpilar(codigo_vader)
    return format_swift_code(codigo_swift)
