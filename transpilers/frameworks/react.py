def transpile_to_react(code):
    """Transpila código Vader a React con JSX - Versión corregida"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_function = False
    in_render = False
    component_name = "MiComponente"
    imports = set()
    hooks_used = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def detect_hooks(line):
        """Detecta hooks de React en el código"""
        if "estado" in line:
            hooks_used.add("useState")
        if "efecto" in line:
            hooks_used.add("useEffect")
    
    # Primera pasada: detectar hooks
    for line in lines:
        detect_hooks(line)
    
    # Agregar imports de React
    react_imports = ["React"]
    if hooks_used:
        react_imports.extend(sorted(hooks_used))
    
    add_line(f"import React, {{ {', '.join(react_imports[1:])} }} from 'react';")
    add_line("")
    
    # Segunda pasada: generar código
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Componente React
        if line.startswith("componente react"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiComponente"
            add_line(f"function {component_name}() {{")
            in_component = True
            indent += 1
            continue

        if line == "fin componente":
            if in_render:
                indent -= 1
                add_line("  );")
                in_render = False
            indent -= 1
            add_line("}")
            add_line("")
            add_line(f"export default {component_name};")
            in_component = False
            continue

        # Estado (useState)
        if line.startswith("estado"):
            parts = line.split("=")
            var_name = parts[0].replace("estado", "").strip()
            initial_value = parts[1].strip() if len(parts) > 1 else "null"
            
            # Capitalizar primera letra para setter
            setter_name = f"set{var_name.capitalize()}"
            add_line(f"const [{var_name}, {setter_name}] = useState({initial_value});")
            continue

        # Establecer estado
        if line.startswith("establecer"):
            parts = line.split("=")
            if len(parts) == 2:
                var_name = parts[0].replace("establecer", "").strip()
                value = parts[1].strip()
                setter_name = f"set{var_name.capitalize()}"
                add_line(f"{setter_name}({value});")
            continue

        # Funciones
        if line.startswith("funcion"):
            func_name = line.split()[1] if len(line.split()) > 1 else "handleFunction"
            add_line(f"const {func_name} = () => {{")
            in_function = True
            indent += 1
            continue

        if line == "fin funcion":
            indent -= 1
            add_line("};")
            in_function = False
            continue

        # useEffect
        if line.startswith("efecto"):
            if "al montar" in line:
                add_line("useEffect(() => {")
                indent += 1
            continue

        if line == "fin efecto":
            indent -= 1
            add_line("}, []);")
            continue

        # Renderizado
        if line.startswith("renderizar"):
            add_line("return (")
            indent += 1
            in_render = True
            continue

        if line == "fin renderizar":
            indent -= 1
            add_line(");")
            in_render = False
            continue

        # Elementos JSX
        if in_render:
            if line.startswith("div"):
                if "clase=" in line:
                    class_name = line.split('clase=')[1].strip().replace('"', '')
                    add_line(f'<div className="{class_name}">')
                else:
                    add_line("<div>")
                indent += 1
                continue

            if line == "fin div":
                indent -= 1
                add_line("</div>")
                continue

            if line.startswith("titulo1"):
                content = line.replace("titulo1", "").strip().replace('"', '')
                add_line(f"<h1>{content}</h1>")
                continue

            if line.startswith("titulo2"):
                content = line.replace("titulo2", "").strip().replace('"', '')
                add_line(f"<h2>{content}</h2>")
                continue

            if line.startswith("texto"):
                content = line.replace("texto", "").strip()
                if "clase=" in content:
                    parts = content.split('clase=')
                    text_content = parts[0].strip().replace('"', '')
                    class_name = parts[1].strip().replace('"', '')
                    add_line(f'<p className="{class_name}">{text_content}</p>')
                else:
                    content = content.replace('"', '')
                    add_line(f"<p>{content}</p>")
                continue

            if line.startswith("boton"):
                content = line.replace("boton", "").strip()
                if "onclick=" in content:
                    parts = content.split("onclick=")
                    button_text = parts[0].strip().replace('"', '')
                    handler = parts[1].strip()
                    add_line(f'<button onClick={{{handler}}}>{button_text}</button>')
                else:
                    content = content.replace('"', '')
                    add_line(f"<button>{content}</button>")
                continue

            if line.startswith("input"):
                props = []
                if "tipo=" in line:
                    input_type = line.split("tipo=")[1].split()[0].replace('"', '')
                    props.append(f'type="{input_type}"')
                if "valor=" in line:
                    value = line.split("valor=")[1].split()[0]
                    props.append(f'value={value}')
                if "placeholder=" in line:
                    placeholder = line.split("placeholder=")[1].split()[0].replace('"', '')
                    props.append(f'placeholder="{placeholder}"')
                if "onChange=" in line:
                    handler = line.split("onChange=")[1].strip()
                    props.append(f'onChange={handler}')
                
                add_line(f'<input {" ".join(props)} />')
                continue

            # Condicionales JSX
            if line.startswith("si"):
                condition = line.replace("si", "").strip()
                add_line(f"{{{condition} && (")
                indent += 1
                continue

            if line == "fin si":
                indent -= 1
                add_line(")}")
                continue

        # Otras líneas (comentarios o código JavaScript)
        if in_function or in_component:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"console.log({message});")
            else:
                add_line(f"// {line}")

    return "\n".join(output)

def transpilar(codigo):
    return transpile_to_react(codigo)

# Funciones auxiliares para el transpilador de React
def get_react_keywords():
    """Retorna las palabras clave de Vader que se mapean a React"""
    return {
        'componente react': 'React component',
        'estado': 'useState hook',
        'establecer': 'state setter',
        'efecto': 'useEffect hook',
        'al montar': 'useEffect on mount',
        'funcion': 'function declaration',
        'renderizar': 'JSX return',
        'div': 'div element',
        'boton': 'button element',
        'input': 'input element',
        'texto': 'text/paragraph',
        'titulo1': 'h1 element',
        'titulo2': 'h2 element',
        'si': 'conditional rendering',
        'onclick': 'onClick handler',
        'onChange': 'onChange handler',
        'clase': 'className prop'
    }
