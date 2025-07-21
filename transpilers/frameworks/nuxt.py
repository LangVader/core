def transpile_to_nuxt(code):
    """Transpila código Vader a Nuxt.js con Vue 3 y Composition API"""
    lines = code.strip().split('\n')
    output = []
    indent = 0
    in_component = False
    in_page = False
    in_layout = False
    in_middleware = False
    in_plugin = False
    in_api = False
    component_name = "MiComponente"
    imports = set()
    composables_used = set()
    nuxt_features = set()
    
    def add_line(text, indent_offset=0):
        current_indent = (indent + indent_offset) * 2
        output.append(" " * current_indent + text)
    
    def add_import(import_statement):
        imports.add(import_statement)
    
    def detect_nuxt_features(line):
        """Detecta características de Nuxt en el código"""
        if "useFetch" in line or "usar fetch" in line:
            nuxt_features.add("useFetch")
        if "useAsyncData" in line or "usar datos async" in line:
            nuxt_features.add("useAsyncData")
        if "useHead" in line or "usar head" in line:
            nuxt_features.add("useHead")
        if "useRoute" in line or "usar ruta" in line:
            nuxt_features.add("useRoute")
        if "useRouter" in line or "usar router" in line:
            nuxt_features.add("useRouter")
        if "useState" in line or "usar estado" in line:
            nuxt_features.add("useState")
        if "useCookie" in line or "usar cookie" in line:
            nuxt_features.add("useCookie")

    # Detectar tipo de archivo
    file_type = "component"
    if any("pagina" in line or "page" in line for line in lines):
        file_type = "page"
    elif any("layout" in line for line in lines):
        file_type = "layout"
    elif any("middleware" in line for line in lines):
        file_type = "middleware"
    elif any("plugin" in line for line in lines):
        file_type = "plugin"
    elif any("api" in line for line in lines):
        file_type = "api"

    # Estructura básica según el tipo de archivo
    if file_type == "api":
        return process_api_route(lines)
    elif file_type == "middleware":
        return process_middleware(lines)
    elif file_type == "plugin":
        return process_plugin(lines)
    
    # Para componentes, páginas y layouts
    template_content = []
    script_content = []
    style_content = []
    
    current_section = "template"
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        detect_nuxt_features(line)

        # Página Nuxt
        if line.startswith("pagina nuxt") or line.startswith("page"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiPagina"
            in_page = True
            file_type = "page"
            continue

        # Layout Nuxt
        if line.startswith("layout nuxt") or line.startswith("layout"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiLayout"
            in_layout = True
            file_type = "layout"
            continue

        # Componente Nuxt
        if line.startswith("componente nuxt"):
            parts = line.split()
            component_name = parts[2] if len(parts) > 2 else "MiComponente"
            in_component = True
            continue

        if line == "fin componente" or line == "fin pagina" or line == "fin layout":
            in_component = False
            in_page = False
            in_layout = False
            continue

        # Template section
        if line.startswith("template") or line.startswith("plantilla"):
            current_section = "template"
            continue

        if line == "fin template" or line == "fin plantilla":
            current_section = "template"
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
            script_content.append(process_nuxt_script_line(line))
        elif current_section == "style":
            style_content.append(line)
        else:
            template_content.append(process_nuxt_template_line(line))

    # Generar template
    add_line("<template>")
    indent = 1
    for line in template_content:
        if line:
            add_line(line)
    add_line("</template>")
    add_line("")
    
    # Generar script
    add_line("<script setup>")
    
    # Agregar imports de Nuxt
    if nuxt_features:
        nuxt_imports = ", ".join(sorted(nuxt_features))
        add_line(f"import {{ {nuxt_imports} }} from '#app';")
        add_line("")
    
    # Agregar imports de Vue si se necesitan
    if composables_used:
        vue_imports = ", ".join(sorted(composables_used))
        add_line(f"import {{ {vue_imports} }} from 'vue';")
        add_line("")
    
    # Agregar imports personalizados
    if imports:
        for imp in sorted(imports):
            add_line(imp)
        add_line("")
    
    # Meta tags para páginas
    if file_type == "page":
        add_line("// Meta tags y SEO")
        add_line("useHead({")
        add_line("  title: 'Mi Página',")
        add_line("  meta: [")
        add_line("    { name: 'description', content: 'Descripción de mi página' }")
        add_line("  ]")
        add_line("});")
        add_line("")
    
    # Agregar contenido del script
    for line in script_content:
        if line:
            add_line(line)
    
    add_line("</script>")
    
    # Generar estilos si existen
    if style_content:
        add_line("")
        add_line("<style scoped>")
        for line in style_content:
            if line:
                add_line(line)
        add_line("</style>")
    
    return "\n".join(output)

def process_nuxt_template_line(line):
    """Procesa una línea del template Nuxt/Vue"""
    if not line.strip():
        return ""
    
    # NuxtLink para navegación
    if line.startswith("enlace") or line.startswith("NuxtLink"):
        if "a" in line:
            parts = line.split("a")
            text = parts[0].replace("enlace", "").strip()
            route = parts[1].strip()
            return f"<NuxtLink to=\"{route}\">{text}</NuxtLink>"
        else:
            return "<NuxtLink to=\"/\">"
    
    if line == "fin enlace":
        return "</NuxtLink>"
    
    # NuxtPage para layouts
    if line.startswith("pagina contenido") or line == "NuxtPage":
        return "<NuxtPage />"
    
    # NuxtLayout
    if line.startswith("usar layout"):
        layout_name = line.split()[2] if len(line.split()) > 2 else "default"
        return f"<NuxtLayout name=\"{layout_name}\">"
    
    if line == "fin layout":
        return "</NuxtLayout>"
    
    # Lazy components
    if line.startswith("componente lazy"):
        component_name = line.split()[2] if len(line.split()) > 2 else "MiComponente"
        return f"<Lazy{component_name} />"
    
    # Client-only components
    if line.startswith("solo cliente"):
        return "<ClientOnly>"
    
    if line == "fin solo cliente":
        return "</ClientOnly>"
    
    # Usar el procesador de Vue para el resto
    return process_vue_template_line(line)

def process_nuxt_script_line(line):
    """Procesa una línea del script Nuxt"""
    if not line.strip():
        return ""
    
    # Composables de Nuxt
    if line.startswith("usar fetch") or line.startswith("useFetch"):
        url = line.split()[2] if len(line.split()) > 2 else "'/api/data'"
        var_name = line.split()[3] if len(line.split()) > 3 else "data"
        return f"const {{ data: {var_name}, pending, error }} = await useFetch({url});"
    
    if line.startswith("usar datos async") or line.startswith("useAsyncData"):
        key = line.split()[3] if len(line.split()) > 3 else "'data'"
        fetcher = line.split()[4] if len(line.split()) > 4 else "() => $fetch('/api/data')"
        return f"const {{ data, pending, error }} = await useAsyncData({key}, {fetcher});"
    
    if line.startswith("usar head") or line.startswith("useHead"):
        return "useHead({"
    
    if line == "fin head":
        return "});"
    
    if line.startswith("usar ruta") or line.startswith("useRoute"):
        return "const route = useRoute();"
    
    if line.startswith("usar router") or line.startswith("useRouter"):
        return "const router = useRouter();"
    
    if line.startswith("usar estado") or line.startswith("useState"):
        key = line.split()[2] if len(line.split()) > 2 else "'state'"
        initial = line.split()[3] if len(line.split()) > 3 else "() => null"
        return f"const state = useState({key}, {initial});"
    
    if line.startswith("usar cookie") or line.startswith("useCookie"):
        name = line.split()[2] if len(line.split()) > 2 else "'cookie'"
        return f"const cookie = useCookie({name});"
    
    # Navegación
    if line.startswith("navegar a"):
        route = line.split()[2] if len(line.split()) > 2 else "'/'"
        return f"await navigateTo({route});"
    
    if line.startswith("redirigir a"):
        route = line.split()[2] if len(line.split()) > 2 else "'/'"
        return f"await navigateTo({route}, {{ redirectCode: 301 }});"
    
    # Server-side rendering
    if line.startswith("solo servidor") or line.startswith("process.server"):
        return "if (process.server) {"
    
    if line.startswith("solo cliente") or line.startswith("process.client"):
        return "if (process.client) {"
    
    if line == "fin proceso":
        return "}"
    
    # Middleware
    if line.startswith("definir middleware"):
        return "definePageMeta({"
    
    if line == "fin middleware":
        return "});"
    
    # Plugins
    if line.startswith("usar plugin"):
        plugin_name = line.split()[2] if len(line.split()) > 2 else "miPlugin"
        return f"const {{ ${plugin_name} }} = useNuxtApp();"
    
    # Runtime config
    if line.startswith("config runtime"):
        return "const config = useRuntimeConfig();"
    
    if line.startswith("config publico"):
        return "const config = useRuntimeConfig().public;"
    
    # Error handling
    if line.startswith("lanzar error"):
        status = line.split()[2] if len(line.split()) > 2 else "500"
        message = line.split()[3:] if len(line.split()) > 3 else ["Error interno"]
        message_str = " ".join(message)
        return f"throw createError({{ statusCode: {status}, statusMessage: '{message_str}' }});"
    
    if line.startswith("manejar error"):
        return "onErrorCaptured((error) => {"
    
    if line == "fin error":
        return "});"
    
    # Usar el procesador de Vue para el resto
    return process_vue_script_line(line)

def process_api_route(lines):
    """Procesa una ruta API de Nuxt"""
    output = []
    
    output.append("export default defineEventHandler(async (event) => {")
    output.append("  const method = getMethod(event);")
    output.append("  const query = getQuery(event);")
    output.append("")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        if line.startswith("api"):
            continue
        
        if line.startswith("GET"):
            output.append("  if (method === 'GET') {")
            output.append("    // Lógica para GET")
            output.append("    return { message: 'GET request' };")
            output.append("  }")
            
        elif line.startswith("POST"):
            output.append("  if (method === 'POST') {")
            output.append("    const body = await readBody(event);")
            output.append("    // Lógica para POST")
            output.append("    return { message: 'POST request', data: body };")
            output.append("  }")
            
        elif line.startswith("PUT"):
            output.append("  if (method === 'PUT') {")
            output.append("    const body = await readBody(event);")
            output.append("    // Lógica para PUT")
            output.append("    return { message: 'PUT request', data: body };")
            output.append("  }")
            
        elif line.startswith("DELETE"):
            output.append("  if (method === 'DELETE') {")
            output.append("    // Lógica para DELETE")
            output.append("    return { message: 'DELETE request' };")
            output.append("  }")
    
    output.append("});")
    return "\n".join(output)

def process_middleware(lines):
    """Procesa un middleware de Nuxt"""
    output = []
    
    output.append("export default defineNuxtRouteMiddleware((to, from) => {")
    output.append("  // Lógica del middleware")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("middleware"):
            continue
        
        if line.startswith("si no autenticado"):
            output.append("  if (!isAuthenticated()) {")
            output.append("    return navigateTo('/login');")
            output.append("  }")
        elif line.startswith("redirigir a"):
            route = line.split()[2] if len(line.split()) > 2 else "'/'"
            output.append(f"  return navigateTo({route});")
        else:
            output.append(f"  // {line}")
    
    output.append("});")
    return "\n".join(output)

def process_plugin(lines):
    """Procesa un plugin de Nuxt"""
    output = []
    
    output.append("export default defineNuxtPlugin(() => {")
    output.append("  // Lógica del plugin")
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("plugin"):
            continue
        
        output.append(f"  // {line}")
    
    output.append("});")
    return "\n".join(output)

# Importar funciones de Vue para reutilizar
def process_vue_template_line(line):
    """Reutiliza el procesador de template de Vue"""
    # Implementación básica - en un proyecto real importarías desde vue.py
    return line

def process_vue_script_line(line):
    """Reutiliza el procesador de script de Vue"""
    # Implementación básica - en un proyecto real importarías desde vue.py
    return line

def transpilar(codigo):
    return transpile_to_nuxt(codigo)

# Funciones auxiliares para el transpilador de Nuxt.js
def get_nuxt_keywords():
    """Retorna las palabras clave de Vader que se mapean a Nuxt.js"""
    return {
        'pagina nuxt': 'Nuxt page',
        'layout nuxt': 'Nuxt layout',
        'componente nuxt': 'Nuxt component',
        'enlace': 'NuxtLink',
        'pagina contenido': 'NuxtPage',
        'usar layout': 'NuxtLayout',
        'componente lazy': 'Lazy component',
        'solo cliente': 'ClientOnly',
        'usar fetch': 'useFetch',
        'usar datos async': 'useAsyncData',
        'usar head': 'useHead',
        'usar ruta': 'useRoute',
        'usar router': 'useRouter',
        'usar estado': 'useState',
        'usar cookie': 'useCookie',
        'navegar a': 'navigateTo',
        'redirigir a': 'redirect',
        'solo servidor': 'process.server',
        'definir middleware': 'definePageMeta',
        'usar plugin': 'useNuxtApp',
        'config runtime': 'useRuntimeConfig',
        'config publico': 'useRuntimeConfig().public',
        'lanzar error': 'createError',
        'manejar error': 'onErrorCaptured',
        'api': 'API route',
        'middleware': 'Nuxt middleware',
        'plugin': 'Nuxt plugin'
    }
