def transpile_to_ruby(code):
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_class = False
    inside_constructor = False
    in_try_block = False
    in_function = False
    needs_file_io = False
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        # Convertir self. a @
        text = text.replace('self.', '@')
        output.append(" " * current_indent + text)

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
                add_line(f"class {name} < {parent}")
            else:
                add_line(f"class {name}")
            in_class = True
            indent += 1
            continue

        if line.startswith("atributo"):
            parts = line.split()
            name = parts[1]
            if "=" in line:
                value = line.split("=", 1)[1].strip()
                add_line(f"@{name} = {value}")
            else:
                add_line(f"@{name} = nil")
            continue

        if line.startswith("constructor"):
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"{param_name.strip()} = {default.strip()}")
                    else:
                        params.append(param.strip())
                add_line(f"def initialize({', '.join(params)})")
            else:
                add_line("def initialize")
            indent += 1
            inside_constructor = True
            continue

        if line.startswith("metodo"):
            parts = line.split()
            name = parts[1]
            if inside_constructor:
                indent -= 1
                add_line("end")
                inside_constructor = False
            
            # Detectar parámetros
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"{param_name.strip()} = {default.strip()}")
                    else:
                        params.append(param.strip())
                add_line(f"def {name}({', '.join(params)})")
            else:
                add_line(f"def {name}")
            indent += 1
            continue

        if line == "fin metodo":
            indent -= 1
            add_line("end")
            continue

        if line == "fin constructor":
            indent -= 1
            add_line("end")
            inside_constructor = False
            continue

        if line == "fin clase":
            if inside_constructor:
                indent -= 1
                add_line("end")
                inside_constructor = False
            indent -= 1
            add_line("end")
            in_class = False
            continue

        if line.startswith("crear"):
            parts = line.split()
            var = parts[1]
            clase = parts[3] if len(parts) > 3 else "Object"
            add_line(f"{var} = {clase}.new")
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
                        params.append(f"{param_name.strip()} = {default.strip()}")
                    else:
                        params.append(param.strip())
                add_line(f"def {name}({', '.join(params)})")
            else:
                name = func_decl.strip() if func_decl.strip() else "unnamed"
                add_line(f"def {name}")
            
            in_function = True
            indent += 1
            continue

        if line == "fin funcion":
            indent -= 1
            add_line("end")
            in_function = False
            continue

        if line.startswith("mostrar"):
            content = line[len("mostrar"):].strip()
            add_line(f"puts {content}")
            continue

        if line.startswith("decir"):
            content = line[len("decir"):].strip()
            add_line(f"puts {content}")
            continue

        if line.startswith("preguntar"):
            content = line[len("preguntar"):].strip()
            add_line(f"print {content}")
            add_line("gets.chomp")
            continue

        if line.startswith("si "):
            condition = line[len("si "):].strip()
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            condition = condition.replace(" y también ", " && ")
            condition = condition.replace(" o también ", " || ")
            add_line(f"if {condition}")
            indent += 1
            continue

        if line == "sino" or line == "si no":
            indent -= 1
            add_line("else")
            indent += 1
            continue

        if line.startswith("sino si") or line.startswith("si no si"):
            condition = line.replace("sino si", "").replace("si no si", "").strip()
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            indent -= 1
            add_line(f"elsif {condition}")
            indent += 1
            continue

        if line == "fin si":
            indent -= 1
            add_line("end")
            continue

        if line.startswith("repetir ") and " veces" in line:
            times = line.split()[1]
            add_line(f"{times}.times do |i|")
            indent += 1
            continue

        if line.startswith("repetir con cada "):
            parts = line.split()
            var = parts[3]
            collection = parts[5]
            add_line(f"{collection}.each do |{var}|")
            indent += 1
            continue

        if line.startswith("repetir mientras "):
            condition = line[len("repetir mientras "):].strip()
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            add_line(f"while {condition}")
            indent += 1
            continue

        if line.startswith("repetir hasta "):
            condition = line[len("repetir hasta "):].strip()
            condition = condition.replace(" es igual a ", " == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            add_line(f"until {condition}")
            indent += 1
            continue

        if line == "fin repetir":
            indent -= 1
            add_line("end")
            continue

        if line.startswith("intentar"):
            add_line("begin")
            indent += 1
            in_try_block = True
            continue

        if line.startswith("capturar"):
            indent -= 1
            if " como " in line:
                error_var = line.split(" como ")[1].strip()
                add_line(f"rescue => {error_var}")
            else:
                add_line("rescue => e")
            indent += 1
            continue

        if line == "finalmente":
            indent -= 1
            add_line("ensure")
            indent += 1
            continue

        if line == "fin intentar":
            indent -= 1
            add_line("end")
            in_try_block = False
            continue

        if line.startswith("retornar") or line.startswith("devolver"):
            value = line.split(None, 1)[1] if len(line.split()) > 1 else ""
            add_line(f"return {value}")
            continue

        if line.startswith("leer archivo"):
            needs_file_io = True
            filename = line[len("leer archivo"):].strip()
            add_line(f"File.read({filename})")
            continue

        if line.startswith("escribir archivo"):
            needs_file_io = True
            parts = line.split(" con ")
            filename = parts[0][len("escribir archivo"):].strip()
            content = parts[1].strip() if len(parts) > 1 else '""'
            add_line(f"File.write({filename}, {content})")
            continue

        # Arrays/Listas
        if line.startswith("lista"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("lista"):].strip()
                values = parts[1].strip()
                add_line(f"{var_name} = [{values}]")
            continue

        if line.startswith("diccionario") or line.startswith("hash"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("diccionario"):].strip() if line.startswith("diccionario") else parts[0][len("hash"):].strip()
                values = parts[1].strip()
                add_line(f"{var_name} = {{{values}}}")
            continue

        # Operaciones con arrays
        if line.startswith("agregar a "):
            parts = line.split()
            array_name = parts[2]
            value = ' '.join(parts[3:]) if len(parts) > 3 else ""
            add_line(f"{array_name} << {value}")
            continue

        if line.startswith("longitud de "):
            array_name = line[len("longitud de "):].strip()
            add_line(f"{array_name}.length")
            continue

        # Bloques
        if line.startswith("bloque"):
            params = ""
            if "(" in line and ")" in line:
                params = line.split("(")[1].split(")")[0].strip()
                params = f"|{params}|" if params else ""
            add_line(f"do {params}")
            indent += 1
            continue

        if line == "fin bloque":
            indent -= 1
            add_line("end")
            continue

        # Símbolos
        if line.startswith("simbolo"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("simbolo"):].strip()
                symbol = parts[1].strip()
                add_line(f"{var_name} = :{symbol}")
            continue

        # Rangos
        if line.startswith("rango"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("rango"):].strip()
                range_def = parts[1].strip()
                if ".." in range_def:
                    start, end = range_def.split("..", 1)
                    add_line(f"{var_name} = {start.strip()}..{end.strip()}")
                continue

        # Expresiones regulares
        if line.startswith("regex"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("regex"):].strip()
                pattern = parts[1].strip()
                add_line(f"{var_name} = /{pattern}/")
            continue

        # Módulos
        if line.startswith("modulo"):
            name = line.split()[1]
            add_line(f"module {name}")
            indent += 1
            continue

        if line == "fin modulo":
            indent -= 1
            add_line("end")
            continue

        # Incluir/Extender módulos
        if line.startswith("incluir"):
            module = line[len("incluir"):].strip()
            add_line(f"include {module}")
            continue

        if line.startswith("extender"):
            module = line[len("extender"):].strip()
            add_line(f"extend {module}")
            continue

        # Require
        if line.startswith("requerir"):
            filename = line[len("requerir"):].strip()
            add_line(f"require {filename}")
            continue

        # Yield
        if line.startswith("ceder"):
            value = line[len("ceder"):].strip()
            if value:
                add_line(f"yield {value}")
            else:
                add_line("yield")
            continue

        # Case/When
        if line.startswith("caso"):
            value = line[len("caso"):].strip()
            add_line(f"case {value}")
            indent += 1
            continue

        if line.startswith("cuando"):
            condition = line[len("cuando"):].strip()
            add_line(f"when {condition}")
            indent += 1
            continue

        if line == "fin caso":
            indent -= 1
            add_line("end")
            continue

        # Lambdas y Procs
        if line.startswith("lambda"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("lambda"):].strip()
                lambda_def = parts[1].strip()
                add_line(f"{var_name} = lambda {{ {lambda_def} }}")
            continue

        if line.startswith("proc"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                var_name = parts[0][len("proc"):].strip()
                proc_def = parts[1].strip()
                add_line(f"{var_name} = proc {{ {proc_def} }}")
            continue

        # Llamadas a funciones
        if line.startswith("llamar"):
            call = line[len("llamar"):].strip()
            if '(' in call and call.endswith(')'):
                add_line(f"{call}")
            elif ' ' in call:
                parts = call.split(' ', 1)
                func_name = parts[0]
                args = parts[1].strip()
                if args.startswith('(') and args.endswith(')'):
                    args = args[1:-1].strip()
                add_line(f"{func_name}({args})")
            else:
                add_line(f"{call}")
            continue

        # Break y Next (continue en Ruby)
        if line == "romper" or line == "salir del repetir":
            add_line("break")
            continue
            
        if line == "continuar" or line == "siguiente":
            add_line("next")
            continue
            
        # Raise (throw en Ruby)
        if line.startswith("lanzar"):
            exception = line[len("lanzar"):].strip()
            add_line(f"raise {exception}")
            continue

        # Conversiones
        if line.startswith("convertir a numero"):
            value = line[len("convertir a numero"):].strip()
            add_line(f"{value}.to_i")
            continue

        if line.startswith("convertir a decimal"):
            value = line[len("convertir a decimal"):].strip()
            add_line(f"{value}.to_f")
            continue

        if line.startswith("convertir a texto"):
            value = line[len("convertir a texto"):].strip()
            add_line(f"{value}.to_s")
            continue

        # Métodos de string
        if line.startswith("mayusculas"):
            value = line[len("mayusculas"):].strip()
            add_line(f"{value}.upcase")
            continue

        if line.startswith("minusculas"):
            value = line[len("minusculas"):].strip()
            add_line(f"{value}.downcase")
            continue

        # Métodos de array
        if line.startswith("mapear"):
            array = line[len("mapear"):].strip()
            add_line(f"{array}.map")
            continue

        if line.startswith("filtrar"):
            array = line[len("filtrar"):].strip()
            add_line(f"{array}.select")
            continue

        if line.startswith("reducir"):
            array = line[len("reducir"):].strip()
            add_line(f"{array}.reduce")
            continue

        # Asignaciones y expresiones
        if "=" in line:
            add_line(f"{line}")
            continue

        # Líneas que no se reconocen se comentan
        add_line(f"# {line}")

    # Cerrar bloques restantes
    while indent > 0:
        indent -= 1
        add_line("end")
    
    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_ruby(codigo)

# Funciones auxiliares para el transpilador de Ruby
def get_ruby_keywords():
    """Retorna las palabras clave de Vader que se mapean a Ruby"""
    return {
        'clase': 'class',
        'modulo': 'module',
        'funcion': 'def',
        'si': 'if',
        'sino': 'else',
        'sino si': 'elsif',
        'repetir': 'loop',
        'mientras': 'while',
        'hasta': 'until',
        'intentar': 'begin',
        'capturar': 'rescue',
        'finalmente': 'ensure',
        'retornar': 'return',
        'mostrar': 'puts',
        'incluir': 'include',
        'extender': 'extend',
        'requerir': 'require',
        'romper': 'break',
        'continuar': 'next',
        'siguiente': 'next',
        'lanzar': 'raise',
        'ceder': 'yield',
        'caso': 'case',
        'cuando': 'when',
        'lambda': 'lambda',
        'proc': 'proc',
        'bloque': 'do',
        'simbolo': 'symbol',
        'rango': 'range',
        'regex': 'regex',
        'convertir a numero': 'to_i',
        'convertir a decimal': 'to_f',
        'convertir a texto': 'to_s',
        'mayusculas': 'upcase',
        'minusculas': 'downcase',
        'mapear': 'map',
        'filtrar': 'select',
        'reducir': 'reduce'
    }
