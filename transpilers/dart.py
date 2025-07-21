def transpile_to_dart(code):
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_class = False
    inside_constructor = False
    in_try_block = False
    needs_io = False
    needs_convert = False
    imports = set()
    in_function = False
    main_function_exists = False

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
            # Detectar tipo si se especifica
            if len(parts) > 3 and parts[2] == "tipo":
                tipo = parts[3]
                type_map = {
                    'numero': 'int',
                    'decimal': 'double',
                    'texto': 'String',
                    'booleano': 'bool',
                    'lista': 'List',
                    'mapa': 'Map',
                    'nulo': 'null'
                }
                dart_type = type_map.get(tipo, tipo)
                if "=" in line:
                    value = line.split("=", 1)[1].strip()
                    add_line(f"{dart_type} {name} = {value};")
                else:
                    add_line(f"{dart_type}? {name};")
            else:
                add_line(f"var {name};")
            continue

        if line.startswith("constructor"):
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        params.append(f"{param_type.strip()} {param_name.strip()}")
                    else:
                        params.append(f"var {param.strip()}")
                class_name = "Constructor"  # Se debería obtener del contexto de clase
                add_line(f"{class_name}({', '.join(params)}) {{")
            else:
                add_line("Constructor() {")
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
            
            # Detectar parámetros con tipos y tipo de retorno
            if "(" in line and ")" in line:
                params_part = line.split("(")[1].split(")")[0].strip()
                params = []
                for param in params_part.split(",") if params_part else []:
                    param = param.strip()
                    if ":" in param:
                        param_name, param_type = param.split(":", 1)
                        type_map = {
                            'numero': 'int',
                            'decimal': 'double',
                            'texto': 'String',
                            'booleano': 'bool',
                            'lista': 'List',
                            'nada': 'void'
                        }
                        dart_type = type_map.get(param_type.strip(), param_type.strip())
                        params.append(f"{dart_type} {param_name.strip()}")
                    else:
                        params.append(f"var {param.strip()}")
                
                # Detectar tipo de retorno
                return_type = "void"
                if "->" in line:
                    return_type = line.split("->")[1].strip()
                    type_map = {
                        'numero': 'int',
                        'decimal': 'double',
                        'texto': 'String',
                        'booleano': 'bool',
                        'lista': 'List',
                        'nada': 'void'
                    }
                    return_type = type_map.get(return_type, return_type)
                
                add_line(f"{return_type} {name}({', '.join(params)}) {{")
            else:
                add_line(f"void {name}() {{")
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
            clase = parts[3] if len(parts) > 3 else "Object"
            add_line(f"var {var} = {clase}();")
            continue

        if line.startswith("variable"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == "tipo":
                var_name = parts[1]
                var_type = parts[3]
                type_map = {
                    'numero': 'int',
                    'decimal': 'double',
                    'texto': 'String',
                    'booleano': 'bool',
                    'lista': 'List',
                    'mapa': 'Map'
                }
                dart_type = type_map.get(var_type, var_type)
                if "=" in line:
                    value = line.split("=", 1)[1].strip()
                    add_line(f"{dart_type} {var_name} = {value};")
                else:
                    add_line(f"{dart_type}? {var_name};")
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
                            type_map = {
                                'numero': 'int',
                                'decimal': 'double',
                                'texto': 'String',
                                'booleano': 'bool'
                            }
                            dart_type = type_map.get(param_type.strip(), param_type.strip())
                            params.append(f"{dart_type} {param_name.strip()} = {default.strip()}")
                        else:
                            type_map = {
                                'numero': 'int',
                                'decimal': 'double',
                                'texto': 'String',
                                'booleano': 'bool'
                            }
                            dart_type = type_map.get(param_type.strip(), param_type.strip())
                            params.append(f"{dart_type} {param_name.strip()}")
                    elif "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"var {param_name.strip()} = {default.strip()}")
                    else:
                        params.append(f"var {param.strip()}")
                
                # Detectar tipo de retorno
                return_type = "void"
                if "->" in func_decl:
                    return_type = func_decl.split("->")[1].strip()
                    type_map = {
                        'numero': 'int',
                        'decimal': 'double',
                        'texto': 'String',
                        'booleano': 'bool',
                        'lista': 'List',
                        'nada': 'void'
                    }
                    return_type = type_map.get(return_type, return_type)
                
                if name == "main" or name == "principal":
                    main_function_exists = True
                    add_line(f"void main() {{")
                else:
                    prefix = "Future<void>" if async_function else return_type
                    add_line(f"{prefix} {name}({', '.join(params)}) {'async ' if async_function else ''}{{")
            else:
                name = func_decl.strip() if func_decl.strip() else "unnamed"
                if name == "main" or name == "principal":
                    main_function_exists = True
                    add_line("void main() {")
                else:
                    prefix = "Future<void>" if async_function else "void"
                    add_line(f"{prefix} {name}() {'async ' if async_function else ''}{{")
            
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
            add_line(f"print({content});")
            continue

        if line.startswith("decir"):
            content = line[len("decir"):].strip()
            add_line(f"print({content});")
            continue

        if line.startswith("preguntar"):
            needs_io = True
            content = line[len("preguntar"):].strip()
            add_line(f"// Pregunta: {content}")
            add_line("// Nota: En Dart usa stdin.readLineSync() para input")
            continue

        if line.startswith("si "):
            condition = line[len("si "):].strip()
            condition = condition.replace(" es igual a ", " == ")
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
            add_line(f"for (int i = 0; i < {times}; i++) {{")
            indent += 1
            continue

        if line.startswith("repetir con cada "):
            parts = line.split()
            var = parts[3]
            collection = parts[5]
            add_line(f"for (var {var} in {collection}) {{")
            indent += 1
            continue

        if line.startswith("repetir mientras "):
            condition = line[len("repetir mientras "):].strip()
            condition = condition.replace(" es igual a ", " == ")
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
                add_line(f"}} catch ({error_var}) {{")
            else:
                add_line("} catch (e) {")
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
            needs_io = True
            filename = line[len("leer archivo"):].strip()
            add_line(f"String content = File({filename}).readAsStringSync();")
            continue

        if line.startswith("escribir archivo"):
            needs_io = True
            parts = line.split(" con ")
            filename = parts[0][len("escribir archivo"):].strip()
            content = parts[1].strip() if len(parts) > 1 else '""'
            add_line(f"File({filename}).writeAsStringSync({content});")
            continue

        # Futures y async/await
        if line.startswith("esperar"):
            expression = line[len("esperar"):].strip()
            add_line(f"await {expression};")
            continue

        # Streams
        if line.startswith("escuchar"):
            stream = line[len("escuchar"):].strip()
            add_line(f"{stream}.listen((data) {{")
            indent += 1
            continue

        if line == "fin escuchar":
            indent -= 1
            add_line("});")
            continue

        # Widgets (Flutter específico)
        if line.startswith("widget"):
            name = line.split()[1]
            add_line(f"class {name} extends StatelessWidget {{")
            indent += 1
            add_line("@override")
            add_line("Widget build(BuildContext context) {")
            indent += 1
            continue

        if line.startswith("widget_estado"):
            name = line.split()[1]
            add_line(f"class {name} extends StatefulWidget {{")
            indent += 1
            add_line("@override")
            add_line(f"_{name}State createState() => _{name}State();")
            indent -= 1
            add_line("}")
            add_line("")
            add_line(f"class _{name}State extends State<{name}> {{")
            indent += 1
            add_line("@override")
            add_line("Widget build(BuildContext context) {")
            indent += 1
            continue

        if line == "fin widget":
            indent -= 1
            add_line("}")
            indent -= 1
            add_line("}")
            continue

        # Importaciones Dart
        if line.startswith("importar"):
            if " como " in line:
                parts = line.split(" como ")
                module = parts[0][len("importar"):].strip()
                alias = parts[1].strip()
                add_import(f"import '{module}' as {alias};")
            else:
                module = line[len("importar"):].strip()
                # Mapear imports comunes
                import_map = {
                    'flutter': 'package:flutter/material.dart',
                    'material': 'package:flutter/material.dart',
                    'cupertino': 'package:flutter/cupertino.dart',
                    'io': 'dart:io',
                    'async': 'dart:async',
                    'convert': 'dart:convert',
                    'math': 'dart:math'
                }
                dart_import = import_map.get(module, module)
                add_import(f"import '{dart_import}';")
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

        # Conversiones de tipo
        if line.startswith("convertir a numero"):
            value = line[len("convertir a numero"):].strip()
            add_line(f"int.parse({value})")
            continue

        if line.startswith("convertir a texto"):
            value = line[len("convertir a texto"):].strip()
            add_line(f"{value}.toString()")
            continue

        # Asignaciones y expresiones
        if "=" in line:
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
    if needs_io:
        import_lines.append("import 'dart:io';")
    if needs_convert:
        import_lines.append("import 'dart:convert';")
    
    # Agregar imports personalizados
    if imports:
        import_lines.extend(list(imports))
    
    # Si no hay función main, agregar una básica
    if not main_function_exists and not in_class:
        if not any("void main()" in line for line in result_lines):
            result_lines.append("")
            result_lines.append("void main() {")
            result_lines.append("  // Código principal aquí")
            result_lines.append("}")
    
    if import_lines:
        result_lines = import_lines + [""] + result_lines
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_dart(codigo)

# Funciones auxiliares para el transpilador de Dart
def get_dart_keywords():
    """Retorna las palabras clave de Vader que se mapean a Dart"""
    return {
        'clase': 'class',
        'widget': 'StatelessWidget',
        'widget_estado': 'StatefulWidget',
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
        'esperar': 'await',
        'escuchar': 'listen',
        'mostrar': 'print',
        'importar': 'import',
        'romper': 'break',
        'continuar': 'continue',
        'lanzar': 'throw',
        'convertir a numero': 'int.parse',
        'convertir a texto': 'toString'
    }
