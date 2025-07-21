def transpile_to_react(code):
    """Transpila código Vader a React con JSX"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_function = False
    component_name = "MiComponente"
    imports = set()
    hooks_used = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    def detect_hooks(line):
        """Detecta hooks de React en el código"""
        if "estado" in line or "useState" in line:
            hooks_used.add("useState")
        if "efecto" in line or "useEffect" in line:
            hooks_used.add("useEffect")
        if "contexto" in line or "useContext" in line:
            hooks_used.add("useContext")
        if "reducer" in line or "useReducer" in line:
            hooks_used.add("useReducer")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        detect_hooks(line)

        # Componentes React
        if line.startswith("componente"):
            parts = line.split()
            component_name = parts[1] if len(parts) > 1 else "MiComponente"
            add_line(f"function {component_name}() {{")
            in_component = True
            indent += 1
            continue

        if line == "fin componente":
            indent -= 1
            add_line("}")
            add_line("")
            add_line(f"export default {component_name};")
            in_component = False
            continue

        # Estados con useState
        if line.startswith("estado"):
            parts = line.split()
            if len(parts) >= 2:
                state_name = parts[1]
                initial_value = "null"
                if "=" in line:
                    initial_value = line.split("=", 1)[1].strip()
                
                setter_name = f"set{state_name.capitalize()}"
                add_line(f"const [{state_name}, {setter_name}] = useState({initial_value});")
            continue

        # Efectos con useEffect
        if line.startswith("efecto"):
            if "cuando" in line:
                # useEffect con dependencias
                deps = line.split("cuando")[1].strip()
                add_line(f"useEffect(() => {{")
                indent += 1
            else:
                # useEffect sin dependencias
                add_line("useEffect(() => {")
                indent += 1
            continue

        if line == "fin efecto":
            indent -= 1
            add_line("}, []);") 
            continue

        # Eventos
        if line.startswith("al hacer click"):
            handler_name = "handleClick"
            if " en " in line:
                element = line.split(" en ")[1].strip()
                handler_name = f"handle{element.capitalize()}Click"
            
            add_line(f"const {handler_name} = () => {{")
            indent += 1
            continue

        if line.startswith("al cambiar"):
            element = line.split("al cambiar")[1].strip() if "al cambiar" in line else "input"
            handler_name = f"handle{element.capitalize()}Change"
            add_line(f"const {handler_name} = (e) => {{")
            indent += 1
            continue

        if line == "fin evento":
            indent -= 1
            add_line("};")
            continue

        # JSX - Renderizado
        if line.startswith("renderizar") or line.startswith("retornar jsx"):
            add_line("return (")
            indent += 1
            continue

        if line == "fin renderizar" or line == "fin jsx":
            indent -= 1
            add_line(");")
            continue

        # Elementos JSX
        if line.startswith("div"):
            content = line[3:].strip() if len(line) > 3 else ""
            if content:
                add_line(f"<div>{content}</div>")
            else:
                add_line("<div>")
                indent += 1
            continue

        if line == "fin div":
            indent -= 1
            add_line("</div>")
            continue

        if line.startswith("boton"):
            content = line[5:].strip() if len(line) > 5 else "Botón"
            if "onclick" in line:
                handler = line.split("onclick")[1].strip()
                add_line(f"<button onClick={{{handler}}}>{content}</button>")
            else:
                add_line(f"<button>{content}</button>")
            continue

        if line.startswith("input"):
            input_type = "text"
            placeholder = ""
            value = ""
            onChange = ""
            
            if "tipo" in line:
                input_type = line.split("tipo")[1].split()[0].strip()
            if "placeholder" in line:
                placeholder = line.split("placeholder")[1].split()[0].strip()
            if "valor" in line:
                value = line.split("valor")[1].split()[0].strip()
            if "onchange" in line:
                onChange = line.split("onchange")[1].strip()
            
            props = []
            props.append(f'type="{input_type}"')
            if placeholder:
                props.append(f'placeholder={placeholder}')
            if value:
                props.append(f'value={{{value}}}')
            if onChange:
                props.append(f'onChange={{{onChange}}}')
            
            add_line(f"<input {' '.join(props)} />")
            continue

        if line.startswith("texto"):
            content = line[5:].strip() if len(line) > 5 else ""
            add_line(f"<p>{content}</p>")
            continue

        if line.startswith("titulo"):
            level = "1"
            content = line[6:].strip() if len(line) > 6 else "Título"
            if line.startswith("titulo1"):
                level = "1"
                content = line[7:].strip()
            elif line.startswith("titulo2"):
                level = "2"
                content = line[7:].strip()
            elif line.startswith("titulo3"):
                level = "3"
                content = line[7:].strip()
            
            add_line(f"<h{level}>{content}</h{level}>")
            continue

        # Lista de elementos
        if line.startswith("lista"):
            add_line("<ul>")
            indent += 1
            continue

        if line == "fin lista":
            indent -= 1
            add_line("</ul>")
            continue

        if line.startswith("elemento"):
            content = line[8:].strip() if len(line) > 8 else ""
            add_line(f"<li>{content}</li>")
            continue

        # Mapeo de arrays
        if line.startswith("mapear"):
            parts = line.split()
            if len(parts) >= 2:
                array_name = parts[1]
                item_name = parts[3] if len(parts) > 3 and parts[2] == "como" else "item"
                add_line(f"{{{array_name}.map(({item_name}, index) => (")
                indent += 1
            continue

        if line == "fin mapear":
            indent -= 1
            add_line("))}}")
            continue

        # Condicionales en JSX
        if line.startswith("si mostrar"):
            condition = line[len("si mostrar"):].strip()
            add_line(f"{{{condition} && (")
            indent += 1
            continue

        if line == "fin si mostrar":
            indent -= 1
            add_line(")}}")
            continue

        # Props
        if line.startswith("props"):
            props_def = line[5:].strip()
            add_line(f"function {component_name}({{{props_def}}}) {{")
            continue

        # Importaciones específicas de React
        if line.startswith("importar react"):
            add_import("import React from 'react';")
            continue

        if line.startswith("importar hook"):
            hook_name = line.split()[2] if len(line.split()) > 2 else "useState"
            add_import(f"import {{ {hook_name} }} from 'react';")
            continue

        # CSS en línea
        if line.startswith("estilo"):
            style_obj = line[6:].strip()
            add_line(f"const styles = {{{style_obj}}};")
            continue

        # Clases CSS
        if line.startswith("clase css"):
            class_name = line[9:].strip()
            add_line(f'className="{class_name}"')
            continue

        # Formularios
        if line.startswith("formulario"):
            add_line("<form>")
            indent += 1
            continue

        if line == "fin formulario":
            indent -= 1
            add_line("</form>")
            continue

        # Navegación (React Router)
        if line.startswith("navegar a"):
            route = line[9:].strip()
            add_import("import { useNavigate } from 'react-router-dom';")
            add_line("const navigate = useNavigate();")
            add_line(f"navigate('{route}');")
            continue

        # Context
        if line.startswith("usar contexto"):
            context_name = line[13:].strip()
            add_import(f"import {{ useContext }} from 'react';")
            add_line(f"const {context_name.lower()} = useContext({context_name});")
            continue

        # Refs
        if line.startswith("referencia"):
            ref_name = line[10:].strip()
            add_import("import { useRef } from 'react';")
            add_line(f"const {ref_name} = useRef(null);")
            continue

        # Asignaciones y expresiones JavaScript normales
        if "=" in line:
            add_line(f"{line};")
            continue

        # Llamadas a funciones
        if line.startswith("llamar"):
            call = line[6:].strip()
            add_line(f"{call};")
            continue

        # Líneas que no se reconocen se comentan
        add_line(f"// {line}")

    # Cerrar bloques restantes
    while indent > 0:
        indent -= 1
        add_line("}")

    # Agregar imports necesarios
    import_lines = []
    
    # Import básico de React
    if in_component or hooks_used:
        if hooks_used:
            hooks_list = ", ".join(sorted(hooks_used))
            import_lines.append(f"import React, {{ {hooks_list} }} from 'react';")
        else:
            import_lines.append("import React from 'react';")
    
    # Agregar imports personalizados
    if imports:
        import_lines.extend(sorted(imports))
    
    if import_lines:
        result_lines = import_lines + [""] + output
    else:
        result_lines = output
    
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_react(codigo)

# Funciones auxiliares para el transpilador de React
def get_react_keywords():
    """Retorna las palabras clave de Vader que se mapean a React"""
    return {
        'componente': 'function component',
        'estado': 'useState',
        'efecto': 'useEffect',
        'props': 'props',
        'renderizar': 'return JSX',
        'div': '<div>',
        'boton': '<button>',
        'input': '<input>',
        'texto': '<p>',
        'titulo': '<h1>',
        'lista': '<ul>',
        'elemento': '<li>',
        'mapear': 'map function',
        'si mostrar': 'conditional rendering',
        'formulario': '<form>',
        'navegar a': 'navigate',
        'usar contexto': 'useContext',
        'referencia': 'useRef',
        'al hacer click': 'onClick handler',
        'al cambiar': 'onChange handler'
    }
