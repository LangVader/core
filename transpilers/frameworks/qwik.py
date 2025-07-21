def transpile_to_qwik(code):
    """Transpila código Vader a Qwik con JavaScript/TypeScript"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_route = False
    component_name = "MiComponente"
    imports = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    # Imports básicos de Qwik
    add_import("import { component$, useSignal, useStore, useTask$, $ } from '@builder.io/qwik'")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Componente Qwik
        if line.startswith("componente qwik"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiComponente"
            add_line("")
            add_line(f"export const {component_name} = component$(() => {{")
            in_component = True
            indent += 1
            continue

        if line == "fin componente":
            add_line("});")
            in_component = False
            indent -= 1
            continue

        # Ruta Qwik
        if line.startswith("ruta qwik"):
            add_import("import { routeLoader$ } from '@builder.io/qwik-city'")
            add_line("")
            add_line("export const useData = routeLoader$(() => {")
            in_route = True
            indent += 1
            continue

        if line == "fin ruta":
            add_line("});")
            add_line("")
            add_line("export default component$(() => {")
            add_line("  const data = useData();")
            add_line("")
            in_route = False
            indent -= 1
            continue

        # Señales (signals)
        if line.startswith("señal"):
            parts = line.split("=")
            if len(parts) == 2:
                signal_name = parts[0].replace("señal", "").strip()
                initial_value = parts[1].strip()
                add_line(f"const {signal_name} = useSignal({initial_value});")
            continue

        if line.startswith("signal"):
            parts = line.split("=")
            if len(parts) == 2:
                signal_name = parts[0].replace("signal", "").strip()
                initial_value = parts[1].strip()
                add_line(f"const {signal_name} = useSignal({initial_value});")
            continue

        # Estado reactivo
        if line.startswith("estado"):
            parts = line.split("=")
            if len(parts) == 2:
                state_name = parts[0].replace("estado", "").strip()
                initial_value = parts[1].strip()
                add_line(f"const {state_name} = useSignal({initial_value});")
            continue

        # Store
        if line.startswith("store"):
            parts = line.split("=")
            if len(parts) == 2:
                store_name = parts[0].replace("store", "").strip()
                initial_value = parts[1].strip()
                add_line(f"const {store_name} = useStore({initial_value});")
            continue

        # Tareas (effects)
        if line.startswith("tarea"):
            add_line("useTask$(({ track }) => {")
            indent += 1
            continue

        if line == "fin tarea":
            add_line("});")
            indent -= 1
            continue

        # Funciones con $
        if line.startswith("funcion"):
            func_name = line.split()[1] if len(line.split()) > 1 else "miFuncion"
            params = ""
            if "(" in line and ")" in line:
                params = line[line.find("("):line.find(")")+1]
            add_line(f"const {func_name} = ${params} => {{")
            indent += 1
            continue

        if line == "fin funcion":
            add_line("};")
            indent -= 1
            continue

        # Establecer valores
        if line.startswith("establecer"):
            parts = line.split("=")
            if len(parts) == 2:
                var_name = parts[0].replace("establecer", "").strip()
                value = parts[1].strip()
                add_line(f"{var_name}.value = {value};")
            continue

        # Renderizar
        if line.startswith("renderizar"):
            add_line("return (")
            indent += 1
            continue

        if line == "fin renderizar":
            indent -= 1
            add_line(");")
            continue

        # Elementos JSX
        if line.startswith("div"):
            classes = ""
            if "clase=" in line:
                class_part = line.split("clase=")[1].strip().replace('"', '')
                classes = f' class="{class_part}"'
            add_line(f"<div{classes}>")
            indent += 1
            continue

        if line == "fin div":
            indent -= 1
            add_line("</div>")
            continue

        if line.startswith("titulo1"):
            content = line.replace("titulo1", "").strip()
            if "{" in content:
                add_line(f"<h1>{content}</h1>")
            else:
                content = content.replace('"', '')
                add_line(f"<h1>{content}</h1>")
            continue

        if line.startswith("titulo2"):
            content = line.replace("titulo2", "").strip()
            if "{" in content:
                add_line(f"<h2>{content}</h2>")
            else:
                content = content.replace('"', '')
                add_line(f"<h2>{content}</h2>")
            continue

        if line.startswith("parrafo"):
            content = line.replace("parrafo", "").strip()
            if "{" in content:
                add_line(f"<p>{content}</p>")
            else:
                content = content.replace('"', '')
                add_line(f"<p>{content}</p>")
            continue

        if line.startswith("boton"):
            onclick = ""
            content = line.replace("boton", "").strip()
            
            if "onclick=" in line:
                parts = line.split("onclick=")
                content = parts[0].replace("boton", "").strip()
                onclick_func = parts[1].strip().replace('"', '').replace("'", '')
                onclick = f' onClick$={{{onclick_func}}}'
            
            content = content.replace('"', '')
            add_line(f"<button{onclick}>{content}</button>")
            continue

        if line.startswith("input"):
            input_type = "text"
            value = ""
            onInput = ""
            placeholder = ""
            
            if "tipo=" in line:
                type_part = line.split("tipo=")[1].split()[0].replace('"', '').replace("'", '')
                input_type = type_part
            
            if "valor=" in line:
                value_part = line.split("valor=")[1].split()[0].replace('"', '').replace("'", '')
                value = f' value={{{value_part}.value}}'
            
            if "onInput=" in line:
                input_part = line.split("onInput=")[1].split()[0].replace('"', '').replace("'", '')
                onInput = f' onInput$={{{input_part}}}'
            
            if "placeholder=" in line:
                placeholder_part = line.split("placeholder=")[1].split()[0].replace('"', '').replace("'", '')
                placeholder = f' placeholder="{placeholder_part}"'
            
            add_line(f"<input type='{input_type}'{value}{onInput}{placeholder} />")
            continue

        # Condicionales
        if line.startswith("si"):
            condition = line.replace("si", "").strip()
            add_line(f"{{{condition} && (")
            indent += 1
            continue

        if line == "fin si":
            indent -= 1
            add_line(")}}")
            continue

        # Bucles
        if line.startswith("para cada"):
            parts = line.split("en")
            if len(parts) == 2:
                item = parts[0].replace("para cada", "").strip()
                array = parts[1].strip()
                add_line(f"{{{array}.map(({item}) => (")
                indent += 1
            continue

        if line == "fin para cada":
            indent -= 1
            add_line("))}}")
            continue

        # Lazy loading
        if line.startswith("componente lazy"):
            component_name_lazy = line.split()[2] if len(line.split()) > 2 else "LazyComponent"
            add_import("import { component$, lazy$ } from '@builder.io/qwik'")
            add_line(f"const {component_name_lazy} = lazy$(() => import('./{component_name_lazy}'));")
            continue

        # Resource
        if line.startswith("recurso"):
            resource_name = line.split()[1] if len(line.split()) > 1 else "miRecurso"
            add_import("import { useResource$, Resource } from '@builder.io/qwik'")
            add_line(f"const {resource_name} = useResource$(async () => {{")
            indent += 1
            continue

        if line == "fin recurso":
            add_line("});")
            indent -= 1
            continue

        # SEO
        if line.startswith("head"):
            add_import("import { useDocumentHead } from '@builder.io/qwik-city'")
            add_line("useDocumentHead(() => ({")
            indent += 1
            continue

        if line == "fin head":
            add_line("}));")
            indent -= 1
            continue

        if line.startswith("titulo"):
            title = line.replace("titulo", "").strip().replace('"', '')
            add_line(f"title: '{title}',")
            continue

        if line.startswith("descripcion"):
            desc = line.replace("descripcion", "").strip().replace('"', '')
            add_line(f"meta: [{{ name: 'description', content: '{desc}' }}],")
            continue

        # Server actions
        if line.startswith("accion servidor"):
            action_name = line.split()[2] if len(line.split()) > 2 else "miAccion"
            add_import("import { routeAction$ } from '@builder.io/qwik-city'")
            add_line(f"export const use{action_name.capitalize()} = routeAction$(async (data) => {{")
            indent += 1
            continue

        if line == "fin accion":
            add_line("});")
            indent -= 1
            continue

        # Otras líneas (comentarios o código JavaScript)
        if in_component or in_route:
            if line.startswith("consola log"):
                message = line.replace("consola log", "").strip()
                add_line(f"console.log({message});")
            elif "=" in line and not line.startswith("//"):
                add_line(f"{line};")
            else:
                add_line(f"// {line}")

    # Agregar imports al inicio
    import_lines = []
    if imports:
        import_lines.extend(sorted(imports))
        import_lines.append("")
    
    result_lines = import_lines + output
    return "\n".join(result_lines)

def transpilar(codigo):
    return transpile_to_qwik(codigo)

# Funciones auxiliares para el transpilador de Qwik
def get_qwik_keywords():
    """Retorna las palabras clave de Vader que se mapean a Qwik"""
    return {
        'componente qwik': 'Qwik component',
        'ruta qwik': 'Qwik route',
        'señal': 'signal (reactive state)',
        'signal': 'signal (reactive state)',
        'estado': 'reactive state',
        'store': 'reactive store',
        'tarea': 'useTask$ (effect)',
        'funcion': 'component function with $',
        'establecer': 'set signal value',
        'renderizar': 'component render',
        'componente lazy': 'lazy loaded component',
        'recurso': 'useResource$',
        'head': 'document head',
        'titulo': 'page title',
        'descripcion': 'page description',
        'accion servidor': 'server action',
        'titulo1': 'h1 element',
        'titulo2': 'h2 element',
        'parrafo': 'paragraph',
        'boton': 'button',
        'input': 'input field',
        'div': 'div container'
    }
