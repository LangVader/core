"""
Transpilador de Vader a Rust
Convierte código Vader (español natural) a código Rust idiomático y seguro
"""

import re

def transpilar(codigo):
    """
    Transpila código Vader a Rust
    Soporta sintaxis natural en español y genera código Rust seguro y eficiente
    """
    
    # Inicializar el código Rust
    rust_code = []
    
    # Headers y imports necesarios
    rust_code.append("// Código generado por Vader - Transpilador a Rust")
    rust_code.append("// Sintaxis natural en español convertida a Rust")
    rust_code.append("")
    
    # Imports comunes de Rust
    imports_needed = set()
    
    # Dividir en líneas y procesar
    lineas = codigo.strip().split('\n')
    indent_level = 0
    in_function = False
    in_struct = False
    in_impl = False
    current_struct = ""
    
    # Variables para tracking
    variables_declared = set()
    functions_declared = set()
    structs_declared = set()
    
    for i, linea in enumerate(lineas):
        linea_original = linea
        linea = linea.strip()
        
        # Saltar líneas vacías y comentarios
        if not linea or linea.startswith('#'):
            if linea.startswith('#'):
                rust_code.append("    " * indent_level + "//" + linea[1:])
            else:
                rust_code.append("")
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
                        formatted_parts.append(f"{{{part}}}")
                format_str = '{}' * len(formatted_parts)
                parts_str = ', '.join(formatted_parts)
                rust_content = f'println!("{format_str}", {parts_str});'
            else:
                if content.startswith('"') and content.endswith('"'):
                    rust_content = f'println!("{content[1:-1]}");'
                else:
                    rust_content = f'println!("{{{content}}}");'
            rust_code.append("    " * indent_level + rust_content)
            continue
        
        # SINTAXIS NATURAL - Preguntar y guardar respuesta
        if linea.startswith('preguntar ') and ' guardar la respuesta en ' in linea:
            parts = linea.split(' guardar la respuesta en ')
            question = parts[0].replace('preguntar ', '').strip()
            var_name = parts[1].strip()
            
            imports_needed.add("use std::io;")
            if question.startswith('"') and question.endswith('"'):
                clean_question = question[1:-1]
            else:
                clean_question = question
            rust_code.append("    " * indent_level + f'println!("{clean_question}");')
            rust_code.append("    " * indent_level + f'let mut {var_name} = String::new();')
            rust_code.append("    " * indent_level + f'io::stdin().read_line(&mut {var_name}).expect("Error al leer entrada");')
            rust_code.append("    " * indent_level + f'let {var_name} = {var_name}.trim();')
            variables_declared.add(var_name)
            continue
        
        # SINTAXIS NATURAL - Conversiones
        if 'convertir a número' in linea:
            parts = linea.split(' = ')
            if len(parts) == 2:
                var_name = parts[0].strip()
                conversion = parts[1].replace('convertir a número', '').strip()
                rust_code.append("    " * indent_level + f'let {var_name}: i32 = {conversion}.parse().unwrap_or(0);')
                variables_declared.add(var_name)
            continue
        
        if 'convertir a texto' in linea:
            parts = linea.split(' = ')
            if len(parts) == 2:
                var_name = parts[0].strip()
                conversion = parts[1].replace('convertir a texto', '').strip()
                rust_code.append("    " * indent_level + f'let {var_name} = {conversion}.to_string();')
                variables_declared.add(var_name)
            continue
        
        # SINTAXIS NATURAL - Definir funciones
        if linea.startswith('hacer ') and (' con ' in linea or linea.endswith('hacer')):
            if ' con ' in linea:
                parts = linea.replace('hacer ', '').split(' con ')
                func_name = parts[0].strip()
                params = parts[1].strip().replace(' y ', ', ')
                rust_code.append("    " * indent_level + f'fn {func_name}({params}: &str) {{')
            else:
                func_name = linea.replace('hacer ', '').strip()
                rust_code.append("    " * indent_level + f'fn {func_name}() {{')
            
            functions_declared.add(func_name)
            indent_level += 1
            in_function = True
            continue
        
        # SINTAXIS NATURAL - Definir structs (clases)
        if linea.startswith('tipo de cosa llamada '):
            struct_name = linea.replace('tipo de cosa llamada ', '').strip()
            if ' hereda ' in struct_name:
                parts = struct_name.split(' hereda ')
                struct_name = parts[0].strip()
                # Rust no tiene herencia tradicional, usamos traits
                rust_code.append("    " * indent_level + f'struct {struct_name} {{')
            else:
                rust_code.append("    " * indent_level + f'struct {struct_name} {{')
            
            current_struct = struct_name
            structs_declared.add(struct_name)
            indent_level += 1
            in_struct = True
            continue
        
        # SINTAXIS NATURAL - Atributos de struct
        if linea.startswith('guardar ') and in_struct:
            attr_name = linea.replace('guardar ', '').strip()
            rust_code.append("    " * indent_level + f'{attr_name}: String,')
            continue
        
        # SINTAXIS NATURAL - Devolver
        if linea.startswith('devolver '):
            value = linea.replace('devolver ', '').strip()
            rust_code.append("    " * indent_level + f'return {value};')
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
            
            rust_code.append("    " * indent_level + f'if {condition} {{')
            indent_level += 1
            continue
        
        if linea == 'si no':
            indent_level -= 1
            rust_code.append("    " * indent_level + '} else {')
            indent_level += 1
            continue
        
        # SINTAXIS NATURAL - Bucles
        if linea.startswith('repetir ') and ' veces' in linea:
            times = linea.replace('repetir ', '').replace(' veces', '').strip()
            rust_code.append("    " * indent_level + f'for _ in 0..{times} {{')
            indent_level += 1
            continue
        
        if linea.startswith('repetir con cada ') and ' en ' in linea:
            parts = linea.replace('repetir con cada ', '').split(' en ')
            item = parts[0].strip()
            collection = parts[1].strip()
            rust_code.append("    " * indent_level + f'for {item} in {collection}.iter() {{')
            indent_level += 1
            continue
        
        if linea.startswith('repetir siempre'):
            rust_code.append("    " * indent_level + 'loop {')
            indent_level += 1
            continue
        
        if linea == 'salir del repetir':
            rust_code.append("    " * indent_level + 'break;')
            continue
        
        # SINTAXIS NATURAL - Terminar bloques
        if linea == 'terminar':
            indent_level -= 1
            if in_function:
                rust_code.append("    " * indent_level + '}')
                in_function = False
            elif in_struct:
                rust_code.append("    " * indent_level + '}')
                in_struct = False
                # Agregar implementación básica
                rust_code.append("")
                rust_code.append(f'impl {current_struct} {{')
                rust_code.append(f'    fn new() -> Self {{')
                rust_code.append(f'        {current_struct} {{')
                # Agregar campos por defecto
                for line in rust_code:
                    if f'{current_struct} {{' in line:
                        break
                rust_code.append(f'        }}')
                rust_code.append(f'    }}')
                rust_code.append(f'}}')
                rust_code.append("")
            else:
                rust_code.append("    " * indent_level + '}')
            continue
        
        # Variables y asignaciones
        if ' = ' in linea and not linea.startswith('si '):
            parts = linea.split(' = ', 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            
            # Detectar tipo de dato
            if value.startswith('"') and value.endswith('"'):
                rust_code.append("    " * indent_level + f'let {var_name} = {value};')
            elif value.startswith('[') and value.endswith(']'):
                rust_code.append("    " * indent_level + f'let {var_name} = vec!{value};')
            elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                rust_code.append("    " * indent_level + f'let {var_name}: i32 = {value};')
            else:
                rust_code.append("    " * indent_level + f'let {var_name} = {value};')
            
            variables_declared.add(var_name)
            continue
        
        # Llamadas a funciones
        if linea.startswith('llamar '):
            func_call = linea.replace('llamar ', '').strip()
            if '(' not in func_call:
                func_call += '()'
            rust_code.append("    " * indent_level + f'{func_call};')
            continue
        
        # Líneas que no coinciden con patrones específicos
        rust_code.append("    " * indent_level + f'// TODO: {linea}')
    
    # Agregar función main si no existe
    if 'fn main()' not in '\n'.join(rust_code):
        rust_code.append("")
        rust_code.append("fn main() {")
        rust_code.append("    // Función principal")
        rust_code.append("}")
    
    # Agregar imports al inicio
    if imports_needed:
        final_code = ["// Imports necesarios"] + list(imports_needed) + [""] + rust_code
    else:
        final_code = rust_code
    
    return '\n'.join(final_code)

def format_rust_code(code):
    """
    Formatea el código Rust generado para mejor legibilidad
    """
    lines = code.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Limpiar espacios extra
        line = line.rstrip()
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

# Función principal de transpilación
def transpilar_a_rust(codigo_vader):
    """
    Función principal que transpila código Vader a Rust
    """
    codigo_rust = transpilar(codigo_vader)
    return format_rust_code(codigo_rust)
