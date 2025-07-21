def transpile_to_typescript(code):
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_class = False
    inside_constructor = False
    in_try_block = False
    needs_fs = False
    needs_readline = False
    imports = set()
    decorators = []
    async_function = False
    in_function = False

    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        text = text.replace('self.', 'this.')
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

        if line.startswith("clase"):
            parts = line.split()
            name = parts[1]
            # Aplicar decoradores si los hay
            for dec in decorators:
                add_line(dec)
            decorators.clear()
            
            # Herencia
            if len(parts) > 3 and parts[2] == "hereda":
                parent = parts[3]
                add_line(f"class {name} extends {parent} {{")
            else:
                add_line(f"class {name} {{")
            in_class = True
            indent += 1
            inside_constructor = True
            continue

        if line.startswith("atributo"):
            parts = line.split()
            name = parts[1]
            # Detectar tipo si se especifica
            if len(parts) > 3 and parts[2] == "tipo":
                tipo = parts[3]
                type_map = {
                    'numero': 'number',
                    'texto': 'string',
                    'booleano': 'boolean',
                    'lista': 'any[]',
                    'diccionario': 'Record<string, any>',
                    'nulo': 'null'
                }
                ts_type = type_map.get(tipo, tipo)
                add_line(f"public {name}: {ts_type} = null;")
            else:
                add_line(f"public {name}: any = null;")
            continue

        if line.startswith("metodo"):
            parts = line.split()
            name = parts[1]
            if inside_constructor:
                inside_constructor = False
            
            # Detectar parámetros con tipos
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                typed_params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        typed_params.append(f"{param_name.strip()}: {param_type.strip()}")
                    else:
                        typed_params.append(f"{param.strip()}: any")
                add_line(f"public {name}({', '.join(typed_params)}): any {{")
            else:
                add_line(f"public {name}(): any {{")
            indent += 1
            continue

        if line == "fin metodo":
            indent -= 1
            add_line("}")
            continue

        if line == "fin clase":
            if inside_constructor:
                inside_constructor = False
            indent -= 1
            add_line("}")
            in_class = False
            continue

        if line.startswith("crear"):
            parts = line.split()
            var = parts[1]
            clase = parts[3] if len(parts) > 3 else "any"
            add_line(f"let {var}: {clase} = new {clase}();")
            continue

        if line.startswith("variable"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == "tipo":
                var_name = parts[1]
                var_type = parts[3]
                type_map = {
                    'numero': 'number',
                    'texto': 'string',
                    'booleano': 'boolean',
                    'lista': 'any[]',
                    'diccionario': 'Record<string, any>'
                }
                ts_type = type_map.get(var_type, var_type)
                if "=" in line:
                    value = line.split("=", 1)[1].strip()
                    add_line(f"let {var_name}: {ts_type} = {value};")
                else:
                    add_line(f"let {var_name}: {ts_type};")
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
                add_line(dec)
            decorators.clear()
            
            if "(" in func_decl and ")" in func_decl:
                name = func_decl.split("(")[0].strip()
                params_part = func_decl.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        if "=" in param_type:
                            param_type, default = param_type.split("=", 1)
                            params.append(f"{param_name.strip()}: {param_type.strip()} = {default.strip()}")
                        else:
                            params.append(f"{param_name.strip()}: {param_type.strip()}")
                    elif "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"{param_name.strip()}: any = {default.strip()}")
                    else:
                        params.append(f"{param.strip()}: any")
                
                # Detectar tipo de retorno
                return_type = "any"
                if "->" in func_decl:
                    return_type = func_decl.split("->")[1].strip()
                    type_map = {
                        'numero': 'number',
                        'texto': 'string',
                        'booleano': 'boolean',
                        'lista': 'any[]',
                        'nada': 'void'
                    }
                    return_type = type_map.get(return_type, return_type)
                
                prefix = "async function" if async_function else "function"
                add_line(f"{prefix} {name}({', '.join(params)}): {return_type} {{")
            else:
                name = func_decl.strip() if func_decl.strip() else "unnamed"
                prefix = "async function" if async_function else "function"
                add_line(f"{prefix} {name}(): any {{")
            
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
            add_line(f"console.log({content});")
            continue

        if line.startswith("decir"):
            content = line[len("decir"):].strip()
            add_line(f"console.log({content});")
            continue

        if line.startswith("preguntar"):
            needs_readline = True
            content = line[len("preguntar"):].strip()
            add_line(f"// Pregunta: {content}")
            add_line("// Nota: En TypeScript necesitas usar readline o prompt para input")
            continue

        if line.startswith("si "):
            condition = line[len("si "):].strip()
            condition = condition.replace(" es igual a ", " === ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
            condition = condition.replace(" y también ", " && ")
            condition = condition.replace(" o también ", " || ")
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
            add_line(f"for (let i: number = 0; i < {times}; i++) {{")
            indent += 1
            continue

        if line.startswith("repetir con cada "):
            parts = line.split()
            var = parts[3]
            collection = parts[5]
            add_line(f"for (let {var} of {collection}) {{")
            indent += 1
            continue

        if line.startswith("repetir mientras "):
            condition = line[len("repetir mientras "):].strip()
            condition = condition.replace(" es igual a ", " === ")
            condition = condition.replace(" es mayor que ", " > ")
            condition = condition.replace(" es menor que ", " < ")
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
                add_line(f"}} catch ({error_var}: any) {{")
            else:
                add_line("} catch (error: any) {")
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
            needs_fs = True
            filename = line[len("leer archivo"):].strip()
            add_line(f"const content: string = fs.readFileSync({filename}, 'utf8');")
            continue

        if line.startswith("escribir archivo"):
            needs_fs = True
            parts = line.split(" con ")
            filename = parts[0][len("escribir archivo"):].strip()
            content = parts[1].strip() if len(parts) > 1 else '""'
            add_line(f"fs.writeFileSync({filename}, {content});")
            continue

        # Interfaces (específico de TypeScript)
        if line.startswith("interfaz"):
            name = line.split()[1]
            add_line(f"interface {name} {{")
            indent += 1
            continue

        if line == "fin interfaz":
            indent -= 1
            add_line("}")
            continue

        # Tipos personalizados
        if line.startswith("tipo"):
            parts = line.split(" = ", 1)
            if len(parts) == 2:
                type_name = parts[0][len("tipo"):].strip()
                type_def = parts[1].strip()
                add_line(f"type {type_name} = {type_def};")
            continue

        # Enums
        if line.startswith("enum"):
            name = line.split()[1]
            add_line(f"enum {name} {{")
            indent += 1
            continue

        if line == "fin enum":
            indent -= 1
            add_line("}")
            continue

        # Importaciones TypeScript
        if line.startswith("importar"):
            if " desde " in line:
                parts = line.split(" desde ")
                what = parts[0][len("importar"):].strip()
                from_where = parts[1].strip()
                if what.startswith("{") and what.endswith("}"):
                    add_import(f"import {what} from {from_where};")
                else:
                    add_import(f"import {what} from {from_where};")
            else:
                module = line[len("importar"):].strip()
                add_import(f"import * as {module.replace('.', '_')} from '{module}';")
            continue

        # Exportaciones
        if line.startswith("exportar"):
            what = line[len("exportar"):].strip()
            if what == "por_defecto":
                add_line("export default")
            else:
                add_line(f"export {what};")
            continue

        # Async/await
        if line.startswith("esperar"):
            expression = line[len("esperar"):].strip()
            add_line(f"await {expression};")
            continue

        # Generadores
        if line.startswith("generar"):
            value = line[len("generar"):].strip()
            add_line(f"yield {value};")
            continue

        # Arrow functions
        if line.startswith("flecha"):
            rest = line[len("flecha"):].strip()
            if " = " in rest:
                name, definition = rest.split(" = ", 1)
                add_line(f"const {name.strip()}: Function = {definition.strip()};")
            continue

        # Template literals
        if line.startswith("plantilla"):
            rest = line[len("plantilla"):].strip()
            if " = " in rest:
                var, template = rest.split(" = ", 1)
                add_line(f"const {var.strip()}: string = {template.strip()};")
            continue

        # Destructuring
        if line.startswith("desestructurar"):
            rest = line[len("desestructurar"):].strip()
            add_line(f"{rest};")
            continue

        # Spread operator
        if line.startswith("expandir"):
            rest = line[len("expandir"):].strip()
            add_line(f"...{rest}")
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
            add_line(f"throw {exception};")
            continue

        # Asignaciones y expresiones
        if "=" in line:
            # Detectar tipos en asignaciones
            if " tipo " in line:
                parts = line.split(" tipo ")
                assignment = parts[0].strip()
                type_info = parts[1].split("=")[0].strip()
                value = line.split("=", 1)[1].strip() if "=" in line else ""
                var_name = assignment.split("=")[0].strip()
                type_map = {
                    'numero': 'number',
                    'texto': 'string',
                    'booleano': 'boolean',
                    'lista': 'any[]',
                    'diccionario': 'Record<string, any>'
                }
                ts_type = type_map.get(type_info, type_info)
                add_line(f"let {var_name}: {ts_type} = {value};")
            else:
                add_line(f"{line};")
            continue

        # Líneas que no se reconocen se comentan
        add_line(f"// {line}")

    # Cerrar bloques restantes
    while indent > 0:
        indent -= 1
        add_line("}")

    result_lines = output
    
    # Agregar imports necesarios
    import_lines = []
    if needs_fs:
        import_lines.append("import * as fs from 'fs';")
    if needs_readline:
        import_lines.append("import * as readline from 'readline';")
    
    # Agregar imports personalizados
    if imports:
        import_lines.extend(list(imports))
    
    if import_lines:
        result_lines = import_lines + [""] + output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_typescript(codigo)

# Funciones auxiliares para el transpilador de TypeScript
def get_typescript_keywords():
    """Retorna las palabras clave de Vader que se mapean a TypeScript"""
    return {
        'clase': 'class',
        'interfaz': 'interface',
        'tipo': 'type',
        'enum': 'enum',
        'funcion': 'function',
        'asincrona funcion': 'async function',
        'si': 'if',
        'sino': 'else',
        'repetir': 'for',
        'mientras': 'while',
        'intentar': 'try',
        'capturar': 'catch',
        'finalmente': 'finally',
        'retornar': 'return',
        'generar': 'yield',
        'esperar': 'await',
        'mostrar': 'console.log',
        'importar': 'import',
        'exportar': 'export',
        'romper': 'break',
        'continuar': 'continue',
        'lanzar': 'throw',
        'flecha': '=>',
        'plantilla': 'template literal',
        'desestructurar': 'destructuring',
        'expandir': 'spread operator'
    }
