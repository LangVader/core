def transpile_to_sveltekit(code):
    """Transpila código Vader a SvelteKit con JavaScript/TypeScript"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_page = False
    in_layout = False
    in_api = False
    in_load = False
    component_name = "MiComponente"
    imports = set()
    sveltekit_features = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    def detect_sveltekit_features(line):
        """Detecta características de SvelteKit en el código"""
        if "load" in line or "cargar" in line:
            sveltekit_features.add("load")
        if "page" in line or "pagina" in line:
            sveltekit_features.add("page")
        if "layout" in line:
            sveltekit_features.add("layout")
        if "goto" in line or "ir a" in line:
            sveltekit_features.add("goto")
        if "invalidate" in line or "invalidar" in line:
            sveltekit_features.add("invalidate")

    # Detectar tipo de archivo SvelteKit
    file_type = "component"
    if any("pagina" in line or "page" in line for line in lines):
        file_type = "page"
    elif any("layout" in line for line in lines):
        file_type = "layout"
    elif any("api" in line for line in lines):
        file_type = "api"
    elif any("load" in line or "cargar" in line for line in lines):
        file_type = "load"

    # Procesar según el tipo de archivo
    if file_type == "api":
        return process_sveltekit_api(lines)
    elif file_type == "load":
        return process_sveltekit_load(lines)
    
    # Para componentes, páginas y layouts
    script_content = []
    template_content = []
    style_content = []
    
    current_section = "template"
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        detect_sveltekit_features(line)

        # Página SvelteKit
        if line.startswith("pagina sveltekit") or line.startswith("page"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiPagina"
            in_page = True
            file_type = "page"
            continue

        # Layout SvelteKit
        if line.startswith("layout sveltekit") or line.startswith("layout"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiLayout"
            in_layout = True
            file_type = "layout"
            continue

        # Componente SvelteKit
        if line.startswith("componente sveltekit"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiComponente"
            in_component = True
            continue

        if line == "fin componente" or line == "fin pagina" or line == "fin layout":
            in_component = False
            in_page = False
            in_layout = False
            continue

        # Script section
        if line.startswith("script") or line.startswith("logica"):
            current_section = "script"
            continue

        if line == "fin script" or line == "fin logica":
            current_section = "template"
            continue

        # Style section
        if line.startswith("estilos") or line.startswith("style"):
            current_section = "style"
            continue

        if line == "fin estilos" or line == "fin style":
            current_section = "template"
            continue

        # Procesar contenido según la sección
        if current_section == "script":
            script_content.append(process_sveltekit_script_line(line))
        elif current_section == "style":
            style_content.append(line)
        else:
            template_content.append(process_sveltekit_template_line(line))

    # Generar template
    add_line("<script>")
    
    # Agregar imports de SvelteKit
    if sveltekit_features:
        kit_imports = []
        if "goto" in sveltekit_features:
            kit_imports.append("goto")
        if "invalidate" in sveltekit_features:
            kit_imports.append("invalidate")
        
        if kit_imports:
            add_line(f"  import {{ {', '.join(kit_imports)} }} from '$app/navigation';")
        
        if "page" in sveltekit_features:
            add_line("  import { page } from '$app/stores';")
        
        if kit_imports or "page" in sveltekit_features:
            add_line("")
    
    # Agregar imports personalizados
    if imports:
        for imp in sorted(imports):
            add_line(f"  {imp}")
        add_line("")
    
    # Agregar contenido del script
    for line in script_content:
        if line:
            add_line(f"  {line}")
    
    add_line("</script>")
    add_line("")
    
    # Generar template
    for line in template_content:
        if line:
            add_line(line)
    
    # Generar estilos si existen
    if style_content:
        add_line("")
        add_line("<style>")
        for line in style_content:
            if line:
                add_line(f"  {line}")
        add_line("</style>")
    
    return "\n".join(output)

def process_sveltekit_template_line(line):
    """Procesa una línea del template SvelteKit"""
    if not line.strip():
        return ""
    
    # Slot para layouts
    if line.startswith("slot contenido") or line == "slot":
        return "<slot />"
    
    # Enlaces con SvelteKit
    if line.startswith("enlace") or line.startswith("link"):
        if "a" in line:
            parts = line.split("a")
            text = parts[0].replace("enlace", "").replace("link", "").strip()
            route = parts[1].strip()
            return f"<a href=\"{route}\">{text}</a>"
        else:
            return "<a href=\"/\">"
    
    if line == "fin enlace":
        return "</a>"
    
    # Formularios SvelteKit
    if line.startswith("formulario"):
        action = ""
        method = "POST"
        
        if "action" in line:
            action = line.split("action")[1].split()[0].strip()
        if "method" in line:
            method = line.split("method")[1].split()[0].strip()
        
        props = []
        if action:
            props.append(f'action="{action}"')
        props.append(f'method="{method}"')
        
        return f"<form {' '.join(props)}>"
    
    if line == "fin formulario":
        return "</form>"
    
    # Error boundaries
    if line.startswith("error"):
        return "{#if $page.error}"
    
    if line == "fin error":
        return "{/if}"
    
    # Usar el procesador de Svelte para el resto
    return process_svelte_template_line(line)

def process_sveltekit_script_line(line):
    """Procesa una línea del script SvelteKit"""
    if not line.strip():
        return ""
    
    # Navegación
    if line.startswith("ir a") or line.startswith("goto"):
        route = line.split()[2] if len(line.split()) > 2 else "'/'"
        return f"goto({route});"
    
    # Invalidación de datos
    if line.startswith("invalidar"):
        url = line.split()[1] if len(line.split()) > 1 else "''"
        return f"invalidate({url});"
    
    # Acceso a datos de la página
    if line.startswith("datos pagina") or line.startswith("page data"):
        return "const data = $page.data;"
    
    if line.startswith("parametros") or line.startswith("params"):
        return "const params = $page.params;"
    
    if line.startswith("url actual") or line.startswith("current url"):
        return "const url = $page.url;"
    
    # Formularios con actions
    if line.startswith("action"):
        action_name = line.split()[1] if len(line.split()) > 1 else "default"
        return f"export const actions = {{"
    
    if line == "fin action":
        return "};"
    
    # Manejo de errores
    if line.startswith("manejar error"):
        return "export function handleError({ error, event }) {"
    
    if line == "fin manejo error":
        return "}"
    
    # Hooks
    if line.startswith("hook"):
        hook_type = line.split()[1] if len(line.split()) > 1 else "handle"
        return f"export async function {hook_type}({{ event, resolve }}) {{"
    
    if line == "fin hook":
        return "}"
    
    # Stores de SvelteKit
    if line.startswith("store navegacion") or line.startswith("navigating"):
        return "import { navigating } from '$app/stores';"
    
    if line.startswith("store actualizado") or line.startswith("updated"):
        return "import { updated } from '$app/stores';"
    
    # Preload
    if line.startswith("precargar") or line.startswith("preload"):
        return "export const prerender = true;"
    
    if line.startswith("ssr"):
        value = line.split()[1] if len(line.split()) > 1 else "true"
        return f"export const ssr = {value};"
    
    if line.startswith("csr"):
        value = line.split()[1] if len(line.split()) > 1 else "true"
        return f"export const csr = {value};"
    
    # Usar el procesador de Svelte para el resto
    return process_svelte_script_line(line)

def process_sveltekit_api(lines):
    """Procesa una ruta API de SvelteKit"""
    output = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        if line.startswith("api"):
            continue
        
        if line.startswith("GET"):
            output.append("export async function GET({ url, params }) {")
            output.append("  // Lógica para GET")
            output.append("  return new Response(JSON.stringify({ message: 'GET request' }), {")
            output.append("    headers: { 'content-type': 'application/json' }")
            output.append("  });")
            output.append("}")
            output.append("")
            
        elif line.startswith("POST"):
            output.append("export async function POST({ request, params }) {")
            output.append("  const data = await request.json();")
            output.append("  // Lógica para POST")
            output.append("  return new Response(JSON.stringify({ message: 'POST request', data }), {")
            output.append("    headers: { 'content-type': 'application/json' }")
            output.append("  });")
            output.append("}")
            output.append("")
            
        elif line.startswith("PUT"):
            output.append("export async function PUT({ request, params }) {")
            output.append("  const data = await request.json();")
            output.append("  // Lógica para PUT")
            output.append("  return new Response(JSON.stringify({ message: 'PUT request', data }), {")
            output.append("    headers: { 'content-type': 'application/json' }")
            output.append("  });")
            output.append("}")
            output.append("")
            
        elif line.startswith("DELETE"):
            output.append("export async function DELETE({ params }) {")
            output.append("  // Lógica para DELETE")
            output.append("  return new Response(JSON.stringify({ message: 'DELETE request' }), {")
            output.append("    headers: { 'content-type': 'application/json' }")
            output.append("  });")
            output.append("}")
            output.append("")
    
    return "\n".join(output)

def process_sveltekit_load(lines):
    """Procesa una función load de SvelteKit"""
    output = []
    
    output.append("export async function load({ params, url, parent }) {")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("load") or line.startswith("cargar"):
            continue
        
        if line.startswith("fetch"):
            url = line.split()[1] if len(line.split()) > 1 else "'/api/data'"
            output.append(f"  const response = await fetch({url});")
            output.append("  const data = await response.json();")
        elif line.startswith("retornar"):
            data = line.split()[1:] if len(line.split()) > 1 else ["{}"]
            data_str = " ".join(data)
            output.append(f"  return {data_str};")
        else:
            output.append(f"  // {line}")
    
    if not any("return" in line for line in output):
        output.append("  return {};")
    
    output.append("}")
    return "\n".join(output)

# Importar funciones de Svelte para reutilizar
def process_svelte_template_line(line):
    """Reutiliza el procesador de template de Svelte"""
    # Implementación básica - en un proyecto real importarías desde svelte.py
    return line

def process_svelte_script_line(line):
    """Reutiliza el procesador de script de Svelte"""
    # Implementación básica - en un proyecto real importarías desde svelte.py
    return line

def transpilar(codigo):
    return transpile_to_sveltekit(codigo)

# Funciones auxiliares para el transpilador de SvelteKit
def get_sveltekit_keywords():
    """Retorna las palabras clave de Vader que se mapean a SvelteKit"""
    return {
        'pagina sveltekit': 'SvelteKit page',
        'layout sveltekit': 'SvelteKit layout',
        'componente sveltekit': 'SvelteKit component',
        'ir a': 'goto navigation',
        'invalidar': 'invalidate data',
        'datos pagina': 'page data',
        'parametros': 'page params',
        'url actual': 'current URL',
        'action': 'form action',
        'manejar error': 'error handler',
        'hook': 'SvelteKit hook',
        'store navegacion': 'navigating store',
        'store actualizado': 'updated store',
        'precargar': 'prerender',
        'ssr': 'server-side rendering',
        'csr': 'client-side rendering',
        'slot contenido': 'slot element',
        'formulario': 'form element',
        'error': 'error boundary',
        'load': 'load function',
        'cargar': 'load function',
        'api': 'API route'
    }
