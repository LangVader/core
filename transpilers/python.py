def transpile_to_python(code):
    lines = [line.rstrip() for line in code.strip().split('\n')]
    output = []
    indent = 0
    in_class = False
    in_function = False
    imports = set()
    decorators = []
    async_function = False

    def add_line(text, indent_level=None, indent_offset=0):
        if indent_level is None:
            indent_level = indent
        current_indent = (indent_level + indent_offset) * 4
        output.append(" " * current_indent + text)
    
    def add_import(module):
        imports.add(module)

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Decoradores
        if line.startswith("decorador"):
            decorator = line.split()[1]
            decorators.append(f"@{decorator}")
            continue

        # Sintaxis súper natural para clases
        if line.startswith("tipo de cosa llamada"):
            # tipo de cosa llamada Persona
            class_name = line[len("tipo de cosa llamada"):].strip()
            add_line(f"class {class_name}:", indent_level=0)
            indent = 1
            in_class = True
            continue
            
        if line.startswith("clase"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == "hereda":
                class_name, parent = parts[1], parts[3]
                add_line(f"class {class_name}({parent}):", indent_level=0)
            else:
                class_name = parts[1]
                add_line(f"class {class_name}:", indent_level=0)
            indent = 1
            in_class = True
            add_line("def __init__(self):", indent_level=1)
            continue

        # Sintaxis natural para atributos
        if line.startswith("guardar") and in_class:
            # guardar nombre, guardar edad
            name = line[len("guardar"):].strip()
            add_line(f"self.{name} = None", indent_level=2)
            continue
            
        if line.startswith("atributo"):
            name = line.split()[1]
            add_line(f"self.{name} = None", indent_level=2)
            continue

        # Sintaxis súper natural para funciones
        if line.startswith("hacer"):
            # hacer cálculo con número1 y número2
            func_decl = line[len("hacer"):].strip()
            if " con " in func_decl:
                name_part, params_part = func_decl.split(" con ", 1)
                name = name_part.strip()
                params = [p.strip() for p in params_part.split(" y ")]
                add_line(f"def {name}({', '.join(params)}):", indent_level=0)
            else:
                name = func_decl.strip()
                add_line(f"def {name}():", indent_level=0)
            indent = 1
            in_function = True
            continue
            
        if line.startswith("asincrona funcion") or line.startswith("funcion asincrona"):
            async_function = True
            func_decl = line.replace("asincrona funcion", "").replace("funcion asincrona", "").strip()
        elif line.startswith("funcion"):
            async_function = False
            func_decl = line[len("funcion"):].strip()
        else:
            func_decl = None
            
        if func_decl is not None:
            # Aplicar decoradores si los hay
            for dec in decorators:
                add_line(dec, indent_level=0)
            decorators.clear()
            
            if "(" in func_decl and ")" in func_decl:
                name = func_decl.split("(")[0].strip()
                params_part = func_decl.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"{param_name.strip()}={default.strip()}")
                    else:
                        params.append(param.strip())
                prefix = "async def" if async_function else "def"
                add_line(f"{prefix} {name}({', '.join(params)}):", indent_level=0)
            else:
                name = func_decl.split()[0] if func_decl.split() else "unnamed"
                prefix = "async def" if async_function else "def"
                add_line(f"{prefix} {name}():", indent_level=0)
            indent = 1
            in_function = True
            continue

        if line == "fin funcion" or (line == "terminar" and in_function):
            indent = 0
            in_function = False
            add_line("", indent_level=0)
            continue

        if line.startswith("devolver"):
            value = line[len("devolver"):].strip()
            add_line(f"return {value}", indent_level=indent)
            continue
            
        if line.startswith("retornar"):
            value = line[len("retornar"):].strip()
            add_line(f"return {value}", indent_level=indent)
            continue
            
        if line.startswith("esperar"):
            value = line[len("esperar"):].strip()
            add_line(f"await {value}", indent_level=indent)
            continue
            
        if line.startswith("generar"):
            value = line[len("generar"):].strip()
            add_line(f"yield {value}", indent_level=indent)
            continue

        # Sintaxis súper natural y fácil
        if line.startswith("decir"):
            value = line[len("decir"):].strip()
            add_line(f"print({value})", indent_level=indent)
            continue
            
        if line.startswith("mostrar"):
            value = line[len("mostrar"):].strip()
            add_line(f"print({value})", indent_level=indent)
            continue

        # Estructuras de datos
        if line.startswith("lista"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                # lista numeros = [1, 2, 3]
                values = " ".join(parts[3:])
                add_line(f"{name} = {values}", indent_level=indent)
            else:
                add_line(f"{name} = []", indent_level=indent)
            continue
            
        if line.startswith("diccionario"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                values = " ".join(parts[3:])
                add_line(f"{name} = {values}", indent_level=indent)
            else:
                add_line(f"{name} = {{}}", indent_level=indent)
            continue
            
        if line.startswith("tupla"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                values = " ".join(parts[3:])
                add_line(f"{name} = {values}", indent_level=indent)
            else:
                add_line(f"{name} = ()", indent_level=indent)
            continue
            
        if line.startswith("conjunto"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                values = " ".join(parts[3:])
                add_line(f"{name} = {values}", indent_level=indent)
            else:
                add_line(f"{name} = set()", indent_level=indent)
            continue

        if line.startswith("agregar"):
            rest = line[len("agregar"):].strip()
            if " a " in rest:
                value, name = rest.split(" a ", 1)
                add_line(f"{name.strip()}.append({value.strip()})", indent_level=indent)
            elif " en " in rest:
                # Para diccionarios: agregar clave:valor en diccionario
                parts = rest.split(" en ", 1)
                key_value = parts[0].strip()
                dict_name = parts[1].strip()
                if ":" in key_value:
                    key, value = key_value.split(":", 1)
                    add_line(f"{dict_name}[{key.strip()}] = {value.strip()}", indent_level=indent)
                else:
                    add_line(f"{dict_name}.add({key_value})", indent_level=indent)
            continue
            
        if line.startswith("quitar"):
            rest = line[len("quitar"):].strip()
            if " de " in rest:
                value, name = rest.split(" de ", 1)
                add_line(f"{name.strip()}.remove({value.strip()})", indent_level=indent)
            continue

        if line.startswith("eliminar"):
            rest = line[len("eliminar"):].strip()
            if " de " in rest:
                value, name = rest.split(" de ", 1)
                add_line(f"{name}.remove({value})", indent_level=indent)
            elif " del " in rest:
                # Para diccionarios: eliminar clave del diccionario
                key, dict_name = rest.split(" del ", 1)
                add_line(f"del {dict_name}[{key.strip()}]", indent_level=indent)
            continue

        # Condicionales naturales
        if line.startswith("si "):
            condition = line[len("si "):].strip()
            # Convertir comparaciones naturales
            condition = condition.replace(" es igual a "," == ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            condition = condition.replace(" es mayor o igual que ", " >= ")
            condition = condition.replace(" es menor o igual que ", " <= ")
            condition = condition.replace(" es diferente de ", " != ")
            condition = condition.replace(" y también ", " and ")
            condition = condition.replace(" o también ", " or ")
            condition = condition.replace(" no es ", " != ")
            condition = condition.replace(" está vacía", " == []")
            condition = condition.replace(" contiene ", " in ")
            add_line(f"if {condition}:", indent_level=indent)
            indent += 1
            continue

        if line == "sino" or line == "si no":
            indent -= 1
            add_line("else:", indent_level=indent)
            indent += 1
            continue

        if line == "fin si":
            if indent > 0:
                indent -= 1
            continue
            
        if line == "terminar" and indent > 0:
            # Solo reducir indentación si estamos en una estructura de control
            indent -= 1
            continue

        if line.startswith("repetir"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit() and "veces" in line:
                # repetir 5 veces
                times = parts[1]
                add_line(f"for _ in range({times}):", indent_level=indent)
                indent += 1
            elif "con cada" in line and " en " in line:
                # repetir con cada nombre en lista
                rest = line[len("repetir con cada"):].strip()
                var, iterable = rest.split(" en ", 1)
                add_line(f"for {var.strip()} in {iterable.strip()}:", indent_level=indent)
                indent += 1
            elif line == "repetir siempre":
                add_line("while True:", indent_level=indent)
                indent += 1
            elif len(parts) >= 4 and parts[2] == "en":
                var, iterable = parts[1], parts[3]
                add_line(f"for {var} in {iterable}:", indent_level=indent)
                indent += 1
            elif len(parts) >= 6 and parts[2] == "desde" and parts[4] == "hasta":
                # repetir i desde 0 hasta 10
                var, start, end = parts[1], parts[3], parts[5]
                add_line(f"for {var} in range({start}, {end}):", indent_level=indent)
                indent += 1
            elif len(parts) >= 4 and parts[1] == "mientras":
                # repetir mientras condicion
                condition = " ".join(parts[2:])
                add_line(f"while {condition}:", indent_level=indent)
                indent += 1
            continue

        if line == "fin repetir" or line == "fin mientras" or (line == "terminar" and indent > 0):
            if indent > 0:
                indent -= 1
            continue
            
        # Control de flujo natural
        if line == "salir del repetir":
            add_line("break", indent_level=indent)
            continue

        if line.startswith("intentar"):
            add_line("try:", indent_level=indent)
            indent += 1
            continue

        if line.startswith("capturar"):
            parts = line.split()
            if len(parts) >= 2:
                error_var = parts[1]
                # Soporte para capturar tipos específicos de errores
                if len(parts) >= 4 and parts[2] == "tipo":
                    error_type = parts[3]
                    if indent > 0:
                        indent -= 1
                    add_line(f"except {error_type} as {error_var}:", indent_level=indent)
                else:
                    if indent > 0:
                        indent -= 1
                    add_line(f"except Exception as {error_var}:", indent_level=indent)
                indent += 1
            continue
            
        if line.startswith("finalmente"):
            if indent > 0:
                indent -= 1
            add_line("finally:", indent_level=indent)
            indent += 1
            continue

        if line == "fin intentar":
            if indent > 0:
                indent -= 1
            continue

        if line.startswith("leer archivo"):
            # Formato: leer archivo "archivo.txt" en variable
            partes = line.split()
            archivo = partes[2]
            variable = partes[4]
            add_line('try:', indent_level=indent)
            add_line(f'    with open({archivo}, "r") as f:', indent_level=indent)
            add_line(f'        {variable} = f.read()', indent_level=indent+1)
            add_line('except Exception as e:', indent_level=indent)
            add_line(f'    print(f\'Error al leer el archivo {archivo}: {{e}}\')', indent_level=indent)
            add_line(f'    {variable} = ""', indent_level=indent)
            continue
            
        if line.startswith("escribir archivo"):
            # Formato: escribir archivo "archivo.txt" con "contenido"
            partes = line.split(" con ")
            archivo = partes[0].split()[2]
            contenido = partes[1].strip()
            add_line('try:', indent_level=indent)
            add_line(f'    with open({archivo}, "w") as f:', indent_level=indent)
            add_line(f'        f.write({contenido})', indent_level=indent+1)
            add_line('except Exception as e:', indent_level=indent)
            add_line(f'    print(f\'Error al escribir en el archivo {archivo}: {{e}}\')', indent_level=indent)
            continue

        # Comprensiones de lista
        if line.startswith("comprension lista"):
            # comprension lista resultado = x*2 para x en numeros si x > 0
            rest = line[len("comprension lista"):].strip()
            parts = rest.split(" = ", 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                expression_part = parts[1].strip()
                # Parsear: x*2 para x en numeros si x > 0
                if " para " in expression_part:
                    expr_parts = expression_part.split(" para ", 1)
                    expression = expr_parts[0].strip()
                    rest_part = expr_parts[1].strip()
                    
                    if " si " in rest_part:
                        loop_part, condition = rest_part.split(" si ", 1)
                        add_line(f"{var_name} = [{expression} for {loop_part.strip()} if {condition.strip()}]", indent_level=indent)
                    else:
                        add_line(f"{var_name} = [{expression} for {rest_part.strip()}]", indent_level=indent)
            continue
            
        # Context managers
        if line.startswith("con"):
            # con open("archivo.txt") como f
            rest = line[len("con"):].strip()
            if " como " in rest:
                context, var = rest.split(" como ", 1)
                add_line(f"with {context.strip()} as {var.strip()}:", indent_level=indent)
                indent += 1
            continue
            
        if line == "fin con":
            if indent > 0:
                indent -= 1
            continue
            
        # Importaciones
        if line.startswith("importar"):
            rest = line[len("importar"):].strip()
            if " como " in rest:
                module, alias = rest.split(" como ", 1)
                add_line(f"import {module.strip()} as {alias.strip()}", indent_level=0)
                add_import(f"import {module.strip()} as {alias.strip()}")
            elif " desde " in rest:
                # desde modulo importar funcion
                parts = rest.split(" desde ", 1)
                if len(parts) == 2:
                    what, module = parts[0].strip(), parts[1].strip()
                    add_line(f"from {module} import {what}", indent_level=0)
                    add_import(f"from {module} import {what}")
            else:
                add_line(f"import {rest}", indent_level=0)
                add_import(f"import {rest}")
            continue
            
        # Preguntar y guardar respuesta (sintaxis natural)
        if line.startswith("preguntar"):
            question = line[len("preguntar"):].strip()
            add_line(f"input({question})", indent_level=indent)
            continue
            
        if line.startswith("guardar la respuesta en"):
            var = line[len("guardar la respuesta en"):].strip()
            # Esta línea debe ir después de una pregunta, así que modificamos la línea anterior
            if output and "input(" in output[-1]:
                # Reemplazar la última línea para incluir la variable
                last_line = output[-1]
                if "input(" in last_line:
                    input_part = last_line.split("input(", 1)[1]
                    output[-1] = f"{var} = input({input_part}"
            continue
            
        # Conversiones naturales
        if line.startswith("convertir") and "a número" in line:
            parts = line.split()
            if len(parts) >= 2:
                var = parts[1]
                add_line(f"{var} = int({var})", indent_level=indent)
            continue
            
        if line.startswith("convertir") and "a texto" in line:
            parts = line.split()
            if len(parts) >= 2:
                var = parts[1]
                add_line(f"{var} = str({var})", indent_level=indent)
            continue
            
        if line.startswith("leer") and not line.startswith("leer archivo"):
            var = line.split()[1]
            add_line(f"{var} = input()", indent_level=indent)
            continue

        if line.startswith("llamar"):
            call = line[len("llamar"):].strip()
            if '(' in call and call.endswith(')'):
                add_line(f"{call}", indent_level=indent)
            elif ' ' in call:
                parts = call.split(' ', 1)
                func_name = parts[0]
                args = parts[1].strip()
                if args.startswith('(') and args.endswith(')'):
                    args = args[1:-1].strip()
                add_line(f"{func_name}({args})", indent_level=indent)
            else:
                add_line(f"{call}()", indent_level=indent)
            continue

        # Lambdas
        if line.startswith("lambda"):
            # lambda x, y: x + y
            rest = line[len("lambda"):].strip()
            add_line(f"lambda {rest}", indent_level=indent)
            continue
            
        # Aserciones
        if line.startswith("afirmar"):
            condition = line[len("afirmar"):].strip()
            if " mensaje " in condition:
                cond, msg = condition.split(" mensaje ", 1)
                add_line(f"assert {cond.strip()}, {msg.strip()}", indent_level=indent)
            else:
                add_line(f"assert {condition}", indent_level=indent)
            continue
            
        # Break y Continue
        if line == "romper":
            add_line("break", indent_level=indent)
            continue
            
        if line == "continuar":
            add_line("continue", indent_level=indent)
            continue
            
        # Pass
        if line == "pasar":
            add_line("pass", indent_level=indent)
            continue
            
        # Global y Nonlocal
        if line.startswith("global"):
            vars_list = line[len("global"):].strip()
            add_line(f"global {vars_list}", indent_level=indent)
            continue
            
        if line.startswith("no_local"):
            vars_list = line[len("no_local"):].strip()
            add_line(f"nonlocal {vars_list}", indent_level=indent)
            continue
            
        # Raise
        if line.startswith("lanzar"):
            exception = line[len("lanzar"):].strip()
            add_line(f"raise {exception}", indent_level=indent)
            continue

        if "=" in line and not line.startswith((' ', '\t')):
            add_line(line, indent_level=indent)
            continue

        add_line(f"# {line}", indent_level=indent)

    # Agregar imports al inicio si los hay
    result_lines = output
    if imports:
        import_lines = list(imports)
        result_lines = import_lines + [""] + output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_python(codigo)

# Funciones auxiliares para el transpilador
def get_python_keywords():
    """Retorna las palabras clave de Vader que se mapean a Python"""
    return {
        'clase': 'class',
        'funcion': 'def', 
        'asincrona funcion': 'async def',
        'si': 'if',
        'sino': 'else',
        'repetir': 'for',
        'mientras': 'while',
        'intentar': 'try',
        'capturar': 'except',
        'finalmente': 'finally',
        'retornar': 'return',
        'generar': 'yield',
        'esperar': 'await',
        'mostrar': 'print',
        'importar': 'import',
        'romper': 'break',
        'continuar': 'continue',
        'pasar': 'pass',
        'lanzar': 'raise',
        'afirmar': 'assert',
        'global': 'global',
        'no_local': 'nonlocal',
        'lambda': 'lambda',
        'con': 'with'
    }
