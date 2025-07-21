"""
Transpilador de Vader a Go (Golang)
Convierte código Vader en español natural a Go idiomático y eficiente
"""

def transpile_to_go(codigo):
    """
    Transpila código Vader a Go
    
    Args:
        codigo (str): Código fuente en Vader
        
    Returns:
        str: Código Go equivalente
    """
    lineas = codigo.strip().split('\n')
    output = []
    imports = set()
    
    # Estado del transpilador
    indent = 0
    in_function = False
    in_struct = False
    in_method = False
    current_struct = ""
    
    def add_line(line, indent_level=0):
        """Agrega una línea con la indentación correcta"""
        if line.strip():
            output.append('\t' * indent_level + line)
        else:
            output.append('')
    
    def add_import(import_stmt):
        """Agrega un import al conjunto de imports"""
        imports.add(import_stmt)
    
    # Agregar imports básicos
    add_import('fmt')
    add_import('strconv')
    add_import('strings')
    add_import('bufio')
    add_import('os')
    
    # Agregar package y función main si no hay funciones definidas
    add_line("package main")
    add_line("")
    
    # Procesar cada línea
    for linea in lineas:
        line = linea.strip()
        
        # Ignorar líneas vacías y comentarios
        if not line or line.startswith('#'):
            if line.startswith('#'):
                add_line(f"// {line[1:].strip()}", indent_level=indent)
            continue
        
        # Sintaxis súper natural para structs (clases)
        if line.startswith("tipo de cosa llamada"):
            struct_name = line[len("tipo de cosa llamada"):].strip()
            add_line(f"type {struct_name} struct {{", indent_level=0)
            in_struct = True
            current_struct = struct_name
            indent = 1
            continue
            
        if line.startswith("clase"):
            parts = line.split()
            if len(parts) >= 2:
                struct_name = parts[1]
                add_line(f"type {struct_name} struct {{", indent_level=0)
                in_struct = True
                current_struct = struct_name
                indent = 1
            continue
        
        # Atributos de struct (sintaxis natural)
        if line.startswith("guardar") and in_struct:
            field_name = line[len("guardar"):].strip()
            # Capitalizar para hacer público en Go
            field_name_cap = field_name.capitalize()
            add_line(f"{field_name_cap} string", indent_level=indent)
            continue
            
        if line.startswith("atributo") and in_struct:
            parts = line.split()
            if len(parts) >= 2:
                field_name = parts[1].capitalize()
                field_type = "string"  # Tipo por defecto
                if len(parts) >= 3:
                    if parts[2] == "numero":
                        field_type = "int"
                    elif parts[2] == "decimal":
                        field_type = "float64"
                    elif parts[2] == "booleano":
                        field_type = "bool"
                add_line(f"{field_name} {field_type}", indent_level=indent)
            continue
        
        # Fin de struct
        if line == "fin clase" or (line == "terminar" and in_struct):
            add_line("}", indent_level=0)
            add_line("", indent_level=0)
            in_struct = False
            indent = 0
            continue
        
        # Métodos de struct (sintaxis natural)
        if line.startswith("hacer") and current_struct and not in_function:
            method_name = line[len("hacer"):].strip()
            method_name_cap = method_name.capitalize()
            add_line(f"func (obj *{current_struct}) {method_name_cap}() {{", indent_level=0)
            in_method = True
            in_function = True
            indent = 1
            continue
        
        # Funciones (sintaxis natural)
        if line.startswith("hacer") and not in_struct:
            func_decl = line[len("hacer"):].strip()
            if " con " in func_decl:
                name_part, params_part = func_decl.split(" con ", 1)
                name = name_part.strip().capitalize()
                params = []
                for param in params_part.split(" y "):
                    param = param.strip()
                    params.append(f"{param} string")  # Tipo por defecto
                add_line(f"func {name}({', '.join(params)}) {{", indent_level=0)
            else:
                name = func_decl.strip().capitalize()
                add_line(f"func {name}() {{", indent_level=0)
            in_function = True
            indent = 1
            continue
            
        if line.startswith("funcion"):
            parts = line.split()
            if len(parts) >= 2:
                func_name = parts[1].capitalize()
                add_line(f"func {func_name}() {{", indent_level=0)
                in_function = True
                indent = 1
            continue
        
        # Fin de función
        if line == "fin funcion" or (line == "terminar" and in_function):
            add_line("}", indent_level=indent-1)
            add_line("", indent_level=0)
            in_function = False
            in_method = False
            indent = 0
            continue
        
        # Return (sintaxis natural)
        if line.startswith("devolver"):
            value = line[len("devolver"):].strip()
            add_line(f"return {value}", indent_level=indent)
            continue
            
        if line.startswith("retornar"):
            value = line[len("retornar"):].strip()
            add_line(f"return {value}", indent_level=indent)
            continue
        
        # Print (sintaxis natural)
        if line.startswith("decir"):
            value = line[len("decir"):].strip()
            # Manejar concatenación de strings en Go
            if '+' in value and not (value.startswith('"') and value.endswith('"')):
                # Convertir concatenación a fmt.Sprintf para manejar tipos mixtos
                parts = [p.strip() for p in value.split('+')]
                format_parts = []
                args = []
                for part in parts:
                    if part.startswith('"') and part.endswith('"'):
                        format_parts.append('%s')
                        args.append(part)
                    elif part.isdigit():
                        format_parts.append('%d')
                        args.append(part)
                    else:
                        format_parts.append('%s')
                        args.append(part)
                format_str = '"' + ''.join(format_parts) + '"'
                if args:
                    add_line(f"fmt.Printf({format_str}, {', '.join(args)})", indent_level=indent)
                    add_line(f"fmt.Println()", indent_level=indent)
                else:
                    add_line(f"fmt.Println({value})", indent_level=indent)
            else:
                add_line(f"fmt.Println({value})", indent_level=indent)
            continue
            
        if line.startswith("mostrar"):
            value = line[len("mostrar"):].strip()
            add_line(f"fmt.Println({value})", indent_level=indent)
            continue
        
        # Input (sintaxis natural)
        if line.startswith("preguntar"):
            question = line[len("preguntar"):].strip()
            add_line(f"fmt.Print({question})", indent_level=indent)
            continue
            
        if line.startswith("guardar la respuesta en"):
            var = line[len("guardar la respuesta en"):].strip()
            add_line(f"reader := bufio.NewReader(os.Stdin)", indent_level=indent)
            add_line(f"{var}, _ := reader.ReadString('\\n')", indent_level=indent)
            add_line(f"{var} = strings.TrimSpace({var})", indent_level=indent)
            continue
            
        if line.startswith("leer"):
            parts = line.split()
            if len(parts) >= 2:
                var = parts[1]
                add_line(f"reader := bufio.NewReader(os.Stdin)", indent_level=indent)
                add_line(f"{var}, _ := reader.ReadString('\\n')", indent_level=indent)
                add_line(f"{var} = strings.TrimSpace({var})", indent_level=indent)
            continue
        
        # Conversiones (sintaxis natural)
        if line.startswith("convertir") and "a número" in line:
            parts = line.split()
            if len(parts) >= 2:
                var = parts[1]
                add_line(f"{var}Int, _ := strconv.Atoi({var})", indent_level=indent)
                # Redeclarar la variable como int
                add_line(f"{var} = strconv.Itoa({var}Int)", indent_level=indent)
            continue
            
        if line.startswith("convertir") and "a texto" in line:
            parts = line.split()
            if len(parts) >= 2:
                var = parts[1]
                add_line(f"{var} = strconv.Itoa({var})", indent_level=indent)
            continue
        
        # Variables y asignaciones
        if "=" in line and not line.startswith((' ', '\t')):
            parts = line.split("=", 1)
            var_name = parts[0].strip()
            value = parts[1].strip()
            
            # Detectar tipo de variable
            if value.startswith('"') and value.endswith('"'):
                add_line(f"var {var_name} string = {value}", indent_level=indent)
            elif value.startswith('[') and value.endswith(']'):
                # Convertir array de Python/JS a slice de Go
                # Extraer elementos del array
                elements = value[1:-1]  # Quitar [ ]
                if elements.strip():
                    go_slice = f"[]string{{{elements}}}"
                else:
                    go_slice = "[]string{}"
                add_line(f"{var_name} := {go_slice}", indent_level=indent)
            elif value.isdigit():
                add_line(f"var {var_name} int = {value}", indent_level=indent)
            else:
                add_line(f"{var_name} := {value}", indent_level=indent)
            continue
        
        # Condicionales (sintaxis natural)
        if line.startswith("si "):
            condition = line[len("si "):].strip()
            # Convertir comparaciones naturales
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            condition = condition.replace(" es mayor o igual que ", " >= ")
            condition = condition.replace(" es menor o igual que ", " <= ")
            condition = condition.replace(" es diferente de ", " != ")
            condition = condition.replace(" y también ", " && ")
            condition = condition.replace(" o también ", " || ")
            condition = condition.replace(" no es ", " != ")
            add_line(f"if {condition} {{", indent_level=indent)
            indent += 1
            continue
        
        if line == "sino" or line == "si no":
            indent -= 1
            add_line("} else {", indent_level=indent)
            indent += 1
            continue
        
        if line == "fin si":
            indent -= 1
            add_line("}", indent_level=indent)
            continue
            
        if line == "terminar" and indent > 0:
            indent -= 1
            add_line("}", indent_level=indent)
            continue
        
        # Bucles (sintaxis natural)
        if line.startswith("repetir"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit() and "veces" in line:
                # repetir 5 veces
                times = parts[1]
                add_line(f"for i := 0; i < {times}; i++ {{", indent_level=indent)
                indent += 1
            elif "con cada" in line and " en " in line:
                # repetir con cada nombre en lista
                rest = line[len("repetir con cada"):].strip()
                var, iterable = rest.split(" en ", 1)
                add_line(f"for _, {var.strip()} := range {iterable.strip()} {{", indent_level=indent)
                indent += 1
            elif line == "repetir siempre":
                add_line("for {", indent_level=indent)
                indent += 1
            continue
        
        if line == "fin repetir" or (line == "terminar" and indent > 0):
            indent -= 1
            add_line("}", indent_level=indent)
            continue
            
        # Control de flujo
        if line == "salir del repetir":
            add_line("break", indent_level=indent)
            continue
            
        if line == "continuar":
            add_line("continue", indent_level=indent)
            continue
        
        # Listas/Slices
        if line.startswith("lista"):
            parts = line.split()
            if len(parts) >= 2:
                name = parts[1]
                if len(parts) > 2 and parts[2] == "=":
                    values = " ".join(parts[3:])
                    add_line(f"var {name} []string = {values}", indent_level=indent)
                else:
                    add_line(f"var {name} []string", indent_level=indent)
            continue
        
        if line.startswith("agregar"):
            rest = line[len("agregar"):].strip()
            if " a " in rest:
                value, name = rest.split(" a ", 1)
                add_line(f"{name.strip()} = append({name.strip()}, {value.strip()})", indent_level=indent)
            continue
        
        # Maps/Diccionarios
        if line.startswith("diccionario"):
            parts = line.split()
            if len(parts) >= 2:
                name = parts[1]
                add_line(f"var {name} map[string]string = make(map[string]string)", indent_level=indent)
            continue
        
        # Manejo de errores básico
        if line.startswith("intentar"):
            add_line("// Try block (Go uses explicit error handling)", indent_level=indent)
            continue
            
        if line.startswith("capturar"):
            add_line("// Catch block (Go uses explicit error handling)", indent_level=indent)
            continue
        
        # Llamadas a funciones/métodos
        if line.startswith("llamar"):
            call = line[len("llamar"):].strip()
            if "." in call:
                # Método de objeto
                add_line(f"{call}", indent_level=indent)
            else:
                # Función normal
                add_line(f"{call}()", indent_level=indent)
            continue
        
        # Crear instancias
        if line.startswith("crear"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == "de":
                var_name = parts[1]
                struct_name = parts[3]
                add_line(f"{var_name} := &{struct_name}{{}}", indent_level=indent)
            continue
        
        # Líneas que no coinciden con ningún patrón
        add_line(f"// {line}", indent_level=indent)
    
    # Agregar función main si no hay funciones definidas
    has_main = any("func main()" in line for line in output)
    has_other_funcs = any("func " in line and "func main()" not in line for line in output)
    
    if not has_main:
        # Encontrar donde insertar main
        main_content = []
        non_main_content = []
        
        for line in output:
            if line.strip() and not line.startswith('package') and not line.startswith('import') and not line.startswith('type') and not (line.startswith('func') and 'func main()' not in line):
                main_content.append('\t' + line if line.strip() else line)
            else:
                non_main_content.append(line)
        
        # Reconstruir output con main
        if main_content:
            non_main_content.append("func main() {")
            non_main_content.extend(main_content)
            non_main_content.append("}")
        
        output = non_main_content
    
    # Agregar imports al inicio
    if imports:
        import_lines = ["import ("]
        for imp in sorted(imports):
            import_lines.append(f'\t"{imp}"')
        import_lines.append(")")
        import_lines.append("")
        
        # Insertar imports después del package
        result_lines = [output[0]] + [""] + import_lines + output[1:]
    else:
        result_lines = output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    """Función principal de transpilación"""
    return transpile_to_go(codigo)

# Funciones auxiliares para el transpilador
def get_go_keywords():
    """Retorna las palabras clave de Vader que se mapean a Go"""
    return {
        # Sintaxis natural
        'decir': 'fmt.Println',
        'preguntar': 'fmt.Print',
        'guardar la respuesta en': 'var',
        'convertir a número': 'strconv.Atoi',
        'convertir a texto': 'strconv.Itoa',
        
        # Estructuras de control
        'si': 'if',
        'sino': 'else',
        'si no': 'else',
        'fin si': '}',
        'repetir': 'for',
        'fin repetir': '}',
        'salir del repetir': 'break',
        'continuar': 'continue',
        
        # Funciones y structs
        'hacer': 'func',
        'tipo de cosa llamada': 'type',
        'devolver': 'return',
        'terminar': '}',
        
        # Comparaciones naturales
        'es igual a': '==',
        'es mayor que': '>',
        'es menor que': '<',
        'es mayor o igual que': '>=',
        'es menor o igual que': '<=',
        'es diferente de': '!=',
        'y también': '&&',
        'o también': '||',
    }

def get_go_types():
    """Retorna los tipos de datos de Go"""
    return {
        'texto': 'string',
        'numero': 'int',
        'decimal': 'float64',
        'booleano': 'bool',
        'lista': '[]string',
        'diccionario': 'map[string]string',
    }

def format_go_code(code):
    """Formatea el código Go generado"""
    lines = code.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Limpiar espacios extra
        line = line.rstrip()
        formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)
