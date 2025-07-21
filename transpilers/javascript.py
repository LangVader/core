def transpile_to_javascript(code):
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

        # Decoradores (como comentarios en JS)
        if line.startswith("decorador"):
            decorator = line.split()[1]
            decorators.append(f"// @{decorator}")
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
            add_line("constructor() {")
            indent += 1
            inside_constructor = True
            continue

        if line.startswith("atributo"):
            name = line.split()[1]
            add_line(f"this.{name} = null;")
            continue

        if line.startswith("metodo"):
            name = line.split()[1]
            if inside_constructor:
                indent -= 1
                add_line("}", -1)
                inside_constructor = False
            add_line(f"{name}() {{")
            indent += 1
            continue

        if line == "fin metodo":
            indent -= 1
            add_line("}")
            continue

        if line == "fin clase":
            if inside_constructor:
                indent -= 1
                add_line("}", -1)
                inside_constructor = False
            indent -= 1
            add_line("}")
            in_class = False
            continue

        if line.startswith("crear"):
            _, var, _, clase = line.split()
            add_line(f"let {var} = new {clase}();")
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
                    if "=" in param:
                        param_name, default = param.split("=", 1)
                        params.append(f"{param_name.strip()} = {default.strip()}")
                    else:
                        params.append(param.strip())
                prefix = "async function" if async_function else "function"
                add_line(f"{prefix} {name}({', '.join(params)}) {{")
            else:
                name = func_decl.strip() if func_decl.strip() else "unnamed"
                prefix = "async function" if async_function else "function"
                add_line(f"{prefix} {name}() {{")
            indent += 1
            in_function = True
            continue

        if line == "fin funcion":
            indent -= 1
            in_function = False
            add_line("}")
            continue

        if line.startswith("retornar"):
            value = line[len("retornar"):].strip()
            add_line(f"return {value};")
            continue
            
        if line.startswith("esperar"):
            value = line[len("esperar"):].strip()
            add_line(f"await {value};")
            continue
            
        if line.startswith("generar"):
            value = line[len("generar"):].strip()
            add_line(f"yield {value};")
            continue

        if line.startswith("mostrar"):
            content = line[len("mostrar"):].strip()
            content = content.replace("str(", "String(")
            if (content.startswith('"') and content.endswith('"')) or (content.startswith("'") and content.endswith("'")):
                content = content[1:-1]
                add_line(f'console.log("{content}");')
            else:
                add_line(f"console.log({content});")
            continue

        # Estructuras de datos
        if line.startswith("lista"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                # lista numeros = [1, 2, 3]
                values = " ".join(parts[3:])
                add_line(f"let {name} = {values};")
            else:
                add_line(f"let {name} = [];")
            continue
            
        if line.startswith("objeto") or line.startswith("diccionario"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                values = " ".join(parts[3:])
                add_line(f"let {name} = {values};")
            else:
                add_line(f"let {name} = {{}};")
            continue
            
        if line.startswith("mapa"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                values = " ".join(parts[3:])
                add_line(f"let {name} = {values};")
            else:
                add_line(f"let {name} = new Map();")
            continue
            
        if line.startswith("conjunto"):
            parts = line.split()
            name = parts[1]
            if len(parts) > 2 and parts[2] == "=":
                values = " ".join(parts[3:])
                add_line(f"let {name} = {values};")
            else:
                add_line(f"let {name} = new Set();")
            continue

        if line.startswith("agregar"):
            rest = line[len("agregar"):].strip()
            if " a " in rest:
                value, name = rest.split(" a ", 1)
                add_line(f"{name}.push({value});")
            elif " en " in rest:
                # Para objetos/mapas: agregar clave:valor en objeto
                parts = rest.split(" en ", 1)
                key_value = parts[0].strip()
                obj_name = parts[1].strip()
                if ":" in key_value:
                    key, value = key_value.split(":", 1)
                    add_line(f"{obj_name}[{key.strip()}] = {value.strip()};")
                else:
                    # Para conjuntos
                    add_line(f"{obj_name}.add({key_value});")
            continue

        if line.startswith("eliminar"):
            rest = line[len("eliminar"):].strip()
            if " de " in rest:
                value, name = rest.split(" de ", 1)
                add_line(f"{name} = {name}.filter(item => item !== {value});")
            elif " del " in rest:
                # Para objetos: eliminar clave del objeto
                key, obj_name = rest.split(" del ", 1)
                add_line(f"delete {obj_name}[{key.strip()}];")
            continue

        if line.startswith("si "):
            condition = line[len("si "):].strip()
            add_line(f"if ({condition}) {{")
            indent += 1
            continue

        if line == "sino":
            indent -= 1
            add_line("} else {")
            indent += 1
            continue

        if line == "fin si":
            indent -= 1
            add_line("}")
            continue

        if line.startswith("repetir"):
            parts = line.split()
            if len(parts) >= 4 and parts[2] == "en":
                var, iterable = parts[1], parts[3]
                add_line(f"for (let {var} of {iterable}) {{")
                indent += 1
            elif len(parts) >= 6 and parts[2] == "desde" and parts[4] == "hasta":
                # repetir i desde 0 hasta 10
                var, start, end = parts[1], parts[3], parts[5]
                add_line(f"for (let {var} = {start}; {var} < {end}; {var}++) {{")
                indent += 1
            elif len(parts) >= 4 and parts[1] == "mientras":
                # repetir mientras condicion
                condition = " ".join(parts[2:])
                add_line(f"while ({condition}) {{")
                indent += 1
            continue

        if line == "fin repetir" or line == "fin mientras":
            indent -= 1
            add_line("}")
            continue

        if line.startswith("intentar"):
            add_line("try {")
            indent += 1
            in_try_block = True
            continue

        if line.startswith("capturar"):
            parts = line.split()
            if len(parts) >= 2:
                error_var = parts[1]
                # Soporte para capturar tipos específicos de errores (como comentario)
                if len(parts) >= 4 and parts[2] == "tipo":
                    error_type = parts[3]
                    indent -= 1
                    add_line(f"}} catch ({error_var}) {{ // {error_type}")
                else:
                    indent -= 1
                    add_line(f"}} catch ({error_var}) {{")
                indent += 1
                in_try_block = False
            continue
            
        if line.startswith("finalmente"):
            indent -= 1
            add_line("} finally {")
            indent += 1
            continue

        if line == "fin intentar":
            indent -= 1
            add_line("}")
            continue

        # Arrow functions
        if line.startswith("flecha"):
            # flecha suma = (a, b) => a + b
            rest = line[len("flecha"):].strip()
            if " = " in rest:
                name, func_def = rest.split(" = ", 1)
                add_line(f"const {name.strip()} = {func_def.strip()};")
            continue
            
        # Template literals
        if line.startswith("plantilla"):
            # plantilla mensaje = `Hola ${nombre}`
            rest = line[len("plantilla"):].strip()
            if " = " in rest:
                var_name, template = rest.split(" = ", 1)
                add_line(f"let {var_name.strip()} = {template.strip()};")
            continue
            
        # Destructuring
        if line.startswith("desestructurar"):
            # desestructurar [a, b] = array
            rest = line[len("desestructurar"):].strip()
            if " = " in rest:
                pattern, source = rest.split(" = ", 1)
                add_line(f"let {pattern.strip()} = {source.strip()};")
            continue
            
        # Spread operator
        if line.startswith("expandir"):
            # expandir ...array
            rest = line[len("expandir"):].strip()
            add_line(f"...{rest}")
            continue
            
        # Promises
        if line.startswith("promesa"):
            # promesa resultado = new Promise((resolve, reject) => { ... })
            rest = line[len("promesa"):].strip()
            if " = " in rest:
                var_name, promise_def = rest.split(" = ", 1)
                add_line(f"let {var_name.strip()} = {promise_def.strip()};")
            continue
            
        # Imports/Exports
        if line.startswith("importar"):
            rest = line[len("importar"):].strip()
            if " desde " in rest:
                # importar { funcion } desde "modulo"
                what, module = rest.split(" desde ", 1)
                add_line(f"import {what.strip()} from {module.strip()};")
                add_import(f"import {what.strip()} from {module.strip()};")
            elif " como " in rest:
                # importar modulo como alias
                module, alias = rest.split(" como ", 1)
                add_line(f"import * as {alias.strip()} from {module.strip()};")
                add_import(f"import * as {alias.strip()} from {module.strip()};")
            else:
                add_line(f"import {rest};")
                add_import(f"import {rest};")
            continue
            
        if line.startswith("exportar"):
            rest = line[len("exportar"):].strip()
            if rest.startswith("por_defecto"):
                value = rest[len("por_defecto"):].strip()
                add_line(f"export default {value};")
            else:
                add_line(f"export {rest};")
            continue
            
        if line.startswith("leer "):
            var = line.split()[1]
            add_line(f"let {var} = prompt();")
            needs_readline = True
            continue

        if line.startswith("escribir archivo"):
            partes = line.split(" con ")
            archivo = partes[0].split()[2]
            contenido = partes[1]
            add_line(f"fs.writeFileSync({archivo}, {contenido});")
            needs_fs = True
            continue

        if line.startswith("leer archivo"):
            partes = line.split(" en ")
            archivo = partes[0].split()[2]
            variable = partes[1]
            add_line(f"let {variable} = '';")
            add_line("try {")
            add_line(f"  {variable} = fs.readFileSync({archivo}, 'utf-8');")
            add_line("} catch (e) {")
            add_line(f"  console.log('Error al leer el archivo:', e.message);")
            add_line("}")
            needs_fs = True
            continue

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

        # Lambdas/Arrow functions inline
        if line.startswith("lambda"):
            # lambda x, y: x + y -> (x, y) => x + y
            rest = line[len("lambda"):].strip()
            if ":" in rest:
                params, body = rest.split(":", 1)
                add_line(f"({params.strip()}) => {body.strip()}")
            continue
            
        # Break y Continue
        if line == "romper":
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
            
        # Console methods
        if line.startswith("consola"):
            rest = line[len("consola"):].strip()
            if rest.startswith("error"):
                msg = rest[len("error"):].strip()
                add_line(f"console.error({msg});")
            elif rest.startswith("advertir"):
                msg = rest[len("advertir"):].strip()
                add_line(f"console.warn({msg});")
            elif rest.startswith("info"):
                msg = rest[len("info"):].strip()
                add_line(f"console.info({msg});")
            continue
            
        # JSON operations
        if line.startswith("json_parsear"):
            rest = line[len("json_parsear"):].strip()
            if " = " in rest:
                var, json_str = rest.split(" = ", 1)
                add_line(f"let {var.strip()} = JSON.parse({json_str.strip()});")
            continue
            
        if line.startswith("json_stringify"):
            rest = line[len("json_stringify"):].strip()
            if " = " in rest:
                var, obj = rest.split(" = ", 1)
                add_line(f"let {var.strip()} = JSON.stringify({obj.strip()});")
            continue

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
    if needs_fs:
        import_lines.append("const fs = require('fs');")
    if needs_readline:
        import_lines.append("const readline = require('readline');")
    
    # Agregar imports personalizados
    if imports:
        import_lines.extend(list(imports))
    
    if import_lines:
        result_lines = import_lines + [""] + output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_javascript(codigo)

# Funciones auxiliares para el transpilador de JavaScript
def get_javascript_keywords():
    """Retorna las palabras clave de Vader que se mapean a JavaScript"""
    return {
        'clase': 'class',
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
        'lambda': '=>',
        'flecha': '=>',
        'con': 'with'
    }
