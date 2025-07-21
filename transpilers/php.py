def transpile_to_php(code):
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_class = False
    inside_constructor = False
    in_try_block = False
    in_function = False
    needs_file_functions = False
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 4
        # Convertir self. a $this->
        text = text.replace('self.', '$this->')
        output.append(" " * current_indent + text)
    
    # Agregar apertura de PHP
    output.append("<?php")
    output.append("")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("clase"):
            parts = line.split()
            name = parts[1]
            
            # Herencia
            if len(parts) > 3 and parts[2] == "hereda":
                parent = parts[3]
                add_line(f"class {name} extends {parent} {{")
            else:
                add_line(f"class {name} {{")
            in_class = True
            indent += 1
            continue

        if line.startswith("atributo"):
            parts = line.split()
            name = parts[1]
            if "=" in line:
                value = line.split("=", 1)[1].strip()
                add_line(f"public ${name} = {value};")
            else:
                add_line(f"public ${name};")
            continue

        if line.startswith("constructor"):
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"${param_name.strip()} = {default.strip()}")
                    else:
                        params.append(f"${param.strip()}")
                add_line(f"public function __construct({', '.join(params)}) {{")
            else:
                add_line("public function __construct() {")
            indent += 1
            inside_constructor = True
            continue

        if line.startswith("metodo"):
            parts = line.split()
            name = parts[1]
            if inside_constructor:
                indent -= 1
                add_line("}")
                inside_constructor = False
            
            # Detectar parámetros
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"${param_name.strip()} = {default.strip()}")
                    else:
                        params.append(f"${param.strip()}")
                add_line(f"public function {name}({', '.join(params)}) {{")
            else:
                add_line(f"public function {name}() {{")
            indent += 1
            continue

        if line == "fin metodo":
            indent -= 1
            add_line("}")
            continue

        if line == "fin constructor":
            indent -= 1
            add_line("}")
            inside_constructor = False
            continue

        if line == "fin clase":
            if inside_constructor:
                indent -= 1
                add_line("}")
                inside_constructor = False
            indent -= 1
            add_line("}")
            in_class = False
            continue

        if line.startswith("crear"):
            parts = line.split()
            var = parts[1]
            clase = parts[3] if len(parts) > 3 else "stdClass"
            add_line(f"${var} = new {clase}();")
            continue

        if line.startswith("funcion"):
            func_decl = line[len("funcion"):].strip()
            
            if "(" in func_decl and ")" in func_decl:
                name = func_decl.split("(")[0].strip()
                params_part = func_decl.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"${param_name.strip()} = {default.strip()}")
                    else:
                        params.append(f"${param.strip()}")
                add_line(f"function {name}({', '.join(params)}) {{")
            else:
                name = func_decl.strip() if func_decl.strip() else "unnamed"
                add_line(f"function {name}() {{")
            
            in_function = True
            indent += 1
            continue

        if line == "fin funcion":
            indent -= 1
            add_line("}")
            in_function = False
            continue

        if line.startswith("mostrar"):
            content = line[len("mostrar"):].strip()
            add_line(f"echo {content};")
            continue

        if line.startswith("decir"):
            content = line[len("decir"):].strip()
            add_line(f"echo {content};")
            continue

        if line.startswith("preguntar"):
            content = line[len("preguntar"):].strip()
            add_line(f"// Pregunta: {content}")
            add_line("// Nota: En PHP usa readline() para input desde consola")
            continue

        if line.startswith("si "):
            condition = line[len("si "):].strip()
            # Convertir variables a formato PHP
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            condition = condition.replace(" y también ", " && ")
            condition = condition.replace(" o también ", " || ")
            # Agregar $ a variables que no lo tienen
            words = condition.split()
            for i, word in enumerate(words):
                if word.isalpha() and word not in ['true', 'false', 'null', 'and', 'or', 'not']:
                    if not word.startswith('$') and not word.startswith('"') and not word.startswith("'"):
                        words[i] = f"${word}"
            condition = ' '.join(words)
            add_line(f"if ({condition}) {{")
            indent += 1
            continue

        if line == "sino" or line == "si no":
            indent -= 1
            add_line("} else {")
            indent += 1
            continue

        if line == "fin si":
            indent -= 1
            add_line("}")
            continue

        if line.startswith("repetir ") and " veces" in line:
            times = line.split()[1]
            add_line(f"for ($i = 0; $i < {times}; $i++) {{")
            indent += 1
            continue

        if line.startswith("repetir con cada "):
            parts = line.split()
            var = parts[3]
            collection = parts[5]
            # Agregar $ si no existe
            if not collection.startswith('$'):
                collection = f"${collection}"
            add_line(f"foreach ({collection} as ${var}) {{")
            indent += 1
            continue

        if line.startswith("repetir mientras "):
            condition = line[len("repetir mientras "):].strip()
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            # Agregar $ a variables
            words = condition.split()
            for i, word in enumerate(words):
                if word.isalpha() and not word.startswith('$'):
                    words[i] = f"${word}"
            condition = ' '.join(words)
            add_line(f"while ({condition}) {{")
            indent += 1
            continue

        if line == "fin repetir":
            indent -= 1
            add_line("}")
            continue

        if line.startswith("intentar"):
            add_line("try {")
            indent += 1
            in_try_block = True
            continue

        if line.startswith("capturar"):
            indent -= 1
            if " como " in line:
                error_var = line.split(" como ")[1].strip()
                add_line(f"}} catch (Exception ${error_var}) {{")
            else:
                add_line("} catch (Exception $e) {")
            indent += 1
            continue

        if line == "finalmente":
            indent -= 1
            add_line("} finally {")
            indent += 1
            continue

        if line == "fin intentar":
            indent -= 1
            add_line("}")
            in_try_block = False
            continue

        if line.startswith("retornar") or line.startswith("devolver"):
            value = line.split(None, 1)[1] if len(line.split()) > 1 else ""
            add_line(f"return {value};")
            continue

        if line.startswith("leer archivo"):
            needs_file_functions = True
            filename = line[len("leer archivo"):].strip()
            add_line(f"$content = file_get_contents({filename});")
            continue

        if line.startswith("escribir archivo"):
            needs_file_functions = True
            parts = line.split(" con ")
            filename = parts[0][len("escribir archivo"):].strip()
            content = parts[1].strip() if len(parts) > 1 else '""'
            add_line(f"file_put_contents({filename}, {content});")
            continue

        # Arrays/Listas
        if line.startswith("lista"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("lista"):].strip()
                values = parts[1].strip()
                add_line(f"${var_name} = array({values});")
            continue

        if line.startswith("diccionario"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("diccionario"):].strip()
                values = parts[1].strip()
                add_line(f"${var_name} = array({values});")
            continue

        # Operaciones con arrays
        if line.startswith("agregar a "):
            parts = line.split()
            array_name = parts[2]
            value = ' '.join(parts[3:]) if len(parts) > 3 else ""
            if not array_name.startswith('$'):
                array_name = f"${array_name}"
            add_line(f"array_push({array_name}, {value});")
            continue

        if line.startswith("longitud de "):
            array_name = line[len("longitud de "):].strip()
            if not array_name.startswith('$'):
                array_name = f"${array_name}"
            add_line(f"count({array_name})")
            continue

        # Conexión a base de datos
        if line.startswith("conectar base_datos"):
            parts = line.split()
            if len(parts) >= 3:
                db_info = ' '.join(parts[2:])
                add_line(f"// Conexión a base de datos: {db_info}")
                add_line("// Usa PDO o mysqli para conectar")
            continue

        if line.startswith("consulta"):
            query = line[len("consulta"):].strip()
            add_line(f"// Ejecutar consulta: {query}")
            add_line("// Usa $pdo->query() o $mysqli->query()")
            continue

        # Sesiones
        if line.startswith("iniciar sesion"):
            add_line("session_start();")
            continue

        if line.startswith("guardar en sesion"):
            parts = line.split(" = ", 1)
            if len(parts) == 2:
                key = parts[0][len("guardar en sesion"):].strip()
                value = parts[1].strip()
                add_line(f"$_SESSION['{key}'] = {value};")
            continue

        if line.startswith("obtener de sesion"):
            key = line[len("obtener de sesion"):].strip()
            add_line(f"$_SESSION['{key}']")
            continue

        # Cookies
        if line.startswith("crear cookie"):
            parts = line.split()
            if len(parts) >= 4:
                name = parts[2]
                value = parts[3]
                add_line(f"setcookie('{name}', {value});")
            continue

        if line.startswith("obtener cookie"):
            name = line[len("obtener cookie"):].strip()
            add_line(f"$_COOKIE['{name}']")
            continue

        # Incluir archivos
        if line.startswith("incluir"):
            filename = line[len("incluir"):].strip()
            add_line(f"include {filename};")
            continue

        if line.startswith("requerir"):
            filename = line[len("requerir"):].strip()
            add_line(f"require {filename};")
            continue

        # Llamadas a funciones
        if line.startswith("llamar"):
            call = line[len("llamar"):].strip()
            if '(' in call and call.endswith(')'):
                add_line(f"{call};")
            elif ' ' in call:
                parts = call.split(' ', 1)
                func_name = parts[0]
                args = parts[1].strip()
                if args.startswith('(') and args.endswith(')'):
                    args = args[1:-1].strip()
                add_line(f"{func_name}({args});")
            else:
                add_line(f"{call}();")
            continue

        # Break y Continue
        if line == "romper" or line == "salir del repetir":
            add_line("break;")
            continue
            
        if line == "continuar":
            add_line("continue;")
            continue
            
        # Throw
        if line.startswith("lanzar"):
            exception = line[len("lanzar"):].strip()
            add_line(f"throw new Exception({exception});")
            continue

        # Conversiones
        if line.startswith("convertir a numero"):
            value = line[len("convertir a numero"):].strip()
            add_line(f"(int){value}")
            continue

        if line.startswith("convertir a texto"):
            value = line[len("convertir a texto"):].strip()
            add_line(f"(string){value}")
            continue

        # Variables globales
        if line.startswith("global"):
            vars_list = line[len("global"):].strip()
            vars_with_dollar = []
            for var in vars_list.split(','):
                var = var.strip()
                if not var.startswith('$'):
                    var = f"${var}"
                vars_with_dollar.append(var)
            add_line(f"global {', '.join(vars_with_dollar)};")
            continue

        # Asignaciones y expresiones
        if "=" in line:
            # Convertir variables a formato PHP
            parts = line.split("=", 1)
            var_part = parts[0].strip()
            value_part = parts[1].strip()
            
            # Agregar $ a la variable si no lo tiene
            if not var_part.startswith('$') and not var_part.startswith('$this->'):
                var_part = f"${var_part}"
            
            add_line(f"{var_part} = {value_part};")
            continue

        # Líneas que no se reconocen se comentan
        add_line(f"// {line}")

    # Cerrar bloques restantes
    while indent > 0:
        indent -= 1
        add_line("}")

    # Agregar cierre de PHP si es necesario
    output.append("")
    output.append("?>")
    
    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_php(codigo)

# Funciones auxiliares para el transpilador de PHP
def get_php_keywords():
    """Retorna las palabras clave de Vader que se mapean a PHP"""
    return {
        'clase': 'class',
        'funcion': 'function',
        'si': 'if',
        'sino': 'else',
        'repetir': 'for',
        'mientras': 'while',
        'intentar': 'try',
        'capturar': 'catch',
        'finalmente': 'finally',
        'retornar': 'return',
        'mostrar': 'echo',
        'incluir': 'include',
        'requerir': 'require',
        'romper': 'break',
        'continuar': 'continue',
        'lanzar': 'throw',
        'global': 'global',
        'lista': 'array',
        'diccionario': 'array',
        'longitud de': 'count',
        'convertir a numero': '(int)',
        'convertir a texto': '(string)'
    }
